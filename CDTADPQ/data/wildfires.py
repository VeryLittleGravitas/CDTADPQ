import os, psycopg2, json
from datetime import datetime
from . import sources

urls = {
    'GeoMAC Large Fire Points': 'https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/1',
    'GeoMAC Fire Perimeters': 'https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/2',
    }

class FirePoint:
    def __init__(self, location, usgs_id, name, contained, discovered, cause, acres):
        assert location['type'] and location['coordinates']
        self.location = location
        self.usgs_id = usgs_id
        self.name = name
        self.contained = contained
        self.discovered = discovered
        self.cause = cause
        self.acres = acres
    
    @property
    def title(self):
        x, y = self.location['coordinates']
        return '{name} fire near {lat:.2f}, {lon:.2f}'.format(lon=x, lat=y, **self.__dict__)
    
    @property
    def description(self):
        x, y = self.location['coordinates']
        return '{acres} acre {name} fire'.format(lon=x, lat=y, **self.__dict__)
    
    @property
    def type(self):
        return 'fire'
    
    @property
    def id(self):
        return self.usgs_id

def store_fire_point(db, fire_point):
    ''' Add fire point to the db if the fire point does not already exist in the db
    '''
    db.execute('SELECT * FROM fire_points WHERE usgs_id = %s', (fire_point.usgs_id,))
    point_exists = db.rowcount
    if not point_exists:
        # Create point with location coordinates for insert
        fire_coordinates = fire_point.location['coordinates']
        coordinates = 'POINT(%s %s)' % (fire_coordinates[0], fire_coordinates[1])

        db.execute('INSERT INTO fire_points (location, usgs_id, name, contained, discovered, cause, acres) VALUES (%s, %s, %s, %s, %s, %s, %s)',
         (coordinates, fire_point.usgs_id, fire_point.name, fire_point.contained, fire_point.discovered, fire_point.cause, fire_point.acres))

def convert_fire_point(feature):
    '''
    '''
    properties = feature['properties']
    usgs_id = properties['uniquefireidentifier']
    name = properties['incidentname']
    contained = properties['percentcontained']
    discovered = datetime.utcfromtimestamp(properties['firediscoverydatetime'] / 1000)
    cause = properties['firecause']
    acres = properties['acres']

    return FirePoint(feature['geometry'], usgs_id, name, contained, discovered, cause, acres)

def get_one_fire(db, usgs_id):
    '''
    '''
    db.execute('''SELECT ST_AsGeoJSON(location) as coordinates_json, *
                  FROM fire_points WHERE usgs_id = %s''',
               (usgs_id, ))
    
    fire_row = db.fetchone()
    location = json.loads(fire_row['coordinates_json'])

    return FirePoint(location, fire_row['usgs_id'], fire_row['name'],
                     fire_row['contained'], fire_row['discovered'],
                     fire_row['cause'], fire_row['acres'])

def get_current_fires(db):
    ''' Return all fires that users should be notified of.
    '''
    # Need to not get all fires, need to get all for today or something?
    db.execute('SELECT ST_AsGeoJSON(location) as coordinates_json, * FROM fire_points')
    fire_rows = db.fetchall()
    fires = []
    for fire_row in fire_rows:
        fire_location = json.loads(fire_row['coordinates_json'])
        fire_point = FirePoint(fire_location, fire_row['usgs_id'], fire_row['name'],
                               fire_row['contained'], fire_row['discovered'], fire_row['cause'],
                               fire_row['acres'])
        fires.append(fire_point)
    return fires

def main():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            for feature in sources.load_esri_source(urls['GeoMAC Large Fire Points']):
                fire = convert_fire_point(feature)
                store_fire_point(db, fire)

if __name__ == '__main__':
    exit(main())
