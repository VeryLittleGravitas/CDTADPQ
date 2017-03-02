import unittest, os, unittest.mock as mock
from datetime import datetime
import psycopg2

from . import recreate
from . import wildfires

class WildfireTests (unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.database_url = os.environ['DATABASE_URL']
        recreate.main(self.database_url)

    
    def test_main(self):
        with mock.patch('CDTADPQ.data.sources.load_esri_source') as load_esri_source:
            wildfires.main()
        
        load_esri_source.assert_called_once_with('https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/1')
    
    def test_convert_fire_point(self):
        fire = wildfires.convert_fire_point({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-95.0780629, 35.7197286]}, 'properties': {'objectid': 1, 'latitude': 35.7197, 'longitude': -95.0781, 'gacc': 'SACC', 'hotlink': 'http://www.nifc.gov/fireInfo/nfn.htm', 'state': 'OK', 'status': 'I', 'irwinid': '{14DD44C2-ACF0-4998-A99B-971BF60E9A11}', 'acres': 1500, 'firecause': 'Human', 'reportdatetime': 1487091600000, 'percentcontained': 49, 'uniquefireidentifier': '2017-OKNEU-170102', 'firediscoverydatetime': 1486984500000, 'complexparentirwinid': None, 'pooresponsibleunit': 'OKNEU', 'incidentname': 'Spike Road', 'iscomplex': 'false', 'irwinmodifiedon': 1487067267000, 'mapsymbol': '1', 'datecurrent': 1487235965000, 'pooownerunit': None, 'owneragency': None, 'fireyear': None, 'localincidentidentifier': None, 'incidenttypecategory': None}})
        
        self.assertEqual(fire.location, {'type': 'Point', 'coordinates': [-95.0780629, 35.7197286]})
        self.assertEqual(fire.usgs_id, '2017-OKNEU-170102')
        self.assertEqual(fire.name, 'Spike Road')
        self.assertEqual(fire.contained, 49)
        self.assertEqual(fire.discovered, datetime(2017, 2, 13, 11, 15))
        self.assertEqual(fire.cause, 'Human')
        self.assertEqual(fire.acres, 1500)

    def test_store_fire_point(self):
        fire = wildfires.convert_fire_point({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-95.0780629, 35.7197286]}, 'properties': {'objectid': 1, 'latitude': 35.7197, 'longitude': -95.0781, 'gacc': 'SACC', 'hotlink': 'http://www.nifc.gov/fireInfo/nfn.htm', 'state': 'OK', 'status': 'I', 'irwinid': '{14DD44C2-ACF0-4998-A99B-971BF60E9A11}', 'acres': 1500, 'firecause': 'Human', 'reportdatetime': 1487091600000, 'percentcontained': 49, 'uniquefireidentifier': '2017-OKNEU-170102', 'firediscoverydatetime': 1486984500000, 'complexparentirwinid': None, 'pooresponsibleunit': 'OKNEU', 'incidentname': 'Spike Road', 'iscomplex': 'false', 'irwinmodifiedon': 1487067267000, 'mapsymbol': '1', 'datecurrent': 1487235965000, 'pooownerunit': None, 'owneragency': None, 'fireyear': None, 'localincidentidentifier': None, 'incidenttypecategory': None}})
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as db:
                # Ensure fire has been added
                wildfires.store_fire_point(db, fire)
                db.execute('SELECT * FROM fire_points WHERE usgs_id = %s', ('2017-OKNEU-170102',))
                self.assertEqual(db.rowcount, 1)

                # Ensure fire has not been added again
                wildfires.store_fire_point(db, fire)
                db.execute('SELECT * FROM fire_points WHERE usgs_id = %s', ('2017-OKNEU-170102',))
                self.assertEqual(db.rowcount, 1)

    def test_get_one_fire(self):
        '''
        '''
        db = unittest.mock.Mock()

        db.fetchone.return_value = dict(
            coordinates_json='{"type": "Point", "coordinates": [-122, 37]}', usgs_id='FIRE', name='Fire',
            contained=0, discovered=None, cause='Bambi', acres=9999
            )

        fire = wildfires.get_one_fire(db, 9999)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT ST_AsGeoJSON(location) as coordinates_json, *\n                  FROM fire_points WHERE usgs_id = %s', (9999, )))

    def test_get_current_fires(self):
        '''
        '''
        db = unittest.mock.Mock()
        db.fetchall.return_value = []

        fires0 = wildfires.get_current_fires(db)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT ST_AsGeoJSON(location) as coordinates_json, * FROM fire_points', ))
        self.assertEqual(len(fires0), 0)

        db.fetchall.return_value = [
            dict(coordinates_json='{"type": "Point", "coordinates": [-122, 37]}', usgs_id='FIRE', name='Fire',
                 contained=0, discovered=None, cause='Bambi', acres=9999)
            ]

        fires1 = wildfires.get_current_fires(db)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT ST_AsGeoJSON(location) as coordinates_json, * FROM fire_points', ))
        self.assertEqual(len(fires1), 1)
