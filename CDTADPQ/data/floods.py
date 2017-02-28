import os, psycopg2, json
from datetime import datetime
from . import sources

urls = {
    'Flood Outlook': 'https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Forecasts_Guidance_Warnings/sig_riv_fld_outlk/MapServer/0',
    }

class FloodPolygon:
    def __init__(self, location, valid_time, outlook, issue_time, start_time, end_time, idp_source, idp_subset):
        assert location['type'] and location['coordinates']
        self.location = location
        self.valid_time = valid_time
        self.outlook = outlook
        self.issue_time = issue_time
        self.start_time = start_time
        self.end_time = end_time
        self.idp_source = idp_source
        self.idp_subset = idp_subset

def store_flood_poly(db, flood_poly):
    ''' Add flood poly to the db if the flood poly does not already exist in the db
    '''
    # Convert input GeoJSON to WKT
    flood_json = json.dumps(flood_poly.location)
    db.execute('SELECT ST_AsText(ST_GeomFromGeoJSON(%s))', (flood_json, ))
    (geography_wkt, ) = db.fetchone()

    db.execute('INSERT INTO flood_polys (location, valid_time, outlook, issue_time, start_time, end_time, idp_source, idp_subset) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
     (geography_wkt, flood_poly.valid_time, flood_poly.outlook, flood_poly.issue_time, flood_poly.start_time, flood_poly.end_time, flood_poly.idp_source, flood_poly.idp_subset))

def convert_flood_poly(feature):
    '''
    '''
    properties = feature['properties']
    valid_time = properties['valid_time']
    outlook = properties['outlook']
    issue_time = datetime.strptime(properties['issue_time'], '%Y-%m-%d %H:%M:%S')
    start_time = datetime.strptime(properties['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(properties['end_time'], '%Y-%m-%d %H:%M:%S')
    idp_source = properties['idp_source']
    idp_subset = properties['idp_subset']
    
    return FloodPolygon(feature['geometry'], valid_time, outlook, issue_time, start_time, end_time, idp_source, idp_subset)

def main():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            for feature in sources.load_esri_source(urls['Flood Outlook']):
                quake = convert_flood_poly(feature)
                store_flood_poly(db, quake)

if __name__ == '__main__':
    exit(main())
