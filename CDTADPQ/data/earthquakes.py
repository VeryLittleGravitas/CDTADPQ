import os, psycopg2
from datetime import datetime
from . import sources

urls = {
    'Earthquakes from last 7 days': 'http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/Earthquakes/EarthquakesFromLastSevenDays/MapServer/0',
    }

class EarthquakePoint:
    def __init__(self, location, quake_id, magnitude, depth, numstations, region, datetime):
        assert location['type'] and location['coordinates']
        self.location = location
        self.quake_id = quake_id
        self.magnitude = magnitude
        self.depth = depth
        self.numstations = numstations
        self.region = region
        self.datetime = datetime

def convert_quake_point(feature):
    '''
    '''
    properties = feature['properties']
    quake_id = properties['eqid']
    magnitude = properties['magnitude']
    depth = properties['depth']
    numstations = properties['numstations']
    region = properties['region']
    quaketime = datetime.utcfromtimestamp(properties['datetime'] / 1000)

    return EarthquakePoint(feature['geometry'], quake_id, magnitude, depth, numstations, region, quaketime)

def main():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            for feature in sources.load_esri_source(urls['Earthquakes from last 7 days']):
                quake = convert_quake_point(feature)
                store_quake_point(db, quake)

if __name__ == '__main__':
    exit(main())
