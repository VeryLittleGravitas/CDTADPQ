import os, psycopg2
from datetime import datetime
from . import sources

urls = {
    'GeoMAC Large Fire Points': 'https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/1',
    'GeoMAC Fire Perimeters': 'https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/2',
    }

class FirePoint:
    def __init__(self, location, unique_id, fire_name, contained, discovered, cause, acres):
        self.location = location
        self.unique_id = unique_id
        self.fire_name = fire_name
        self.contained = contained
        self.discovered = discovered
        self.cause = cause
        self.acres = acres

def convert_fire_point(feature):
    '''
    '''
    properties = feature['properties']
    unique_id = properties['uniquefireidentifier']
    fire_name = properties['incidentname']
    contained = properties['percentcontained']
    discovered = datetime.utcfromtimestamp(properties['firediscoverydatetime'] / 1000)
    cause = properties['firecause']
    acres = properties['acres']

    return FirePoint(feature['geometry'], unique_id, fire_name, contained, discovered, cause, acres)

def main():
    for feature in sources.load_esri_source(urls['GeoMAC Large Fire Points']):
        fire = convert_fire_point(feature)
        print(feature)
        print(fire)

if __name__ == '__main__':
    exit(main())
