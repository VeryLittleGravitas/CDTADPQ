import unittest, os, unittest.mock as mock
from datetime import datetime
import psycopg2

from . import recreate
from . import floods

class FloodTests (unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.database_url = os.environ['DATABASE_URL']
        recreate.main(self.database_url)
    
    def test_main(self):
        with mock.patch('CDTADPQ.data.sources.load_esri_source') as load_esri_source:
            floods.main()
        
        load_esri_source.assert_called_once_with('https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Forecasts_Guidance_Warnings/sig_riv_fld_outlk/MapServer/0')
    
    def test_convert_flood_poly(self):
        flood = floods.convert_flood_poly({"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-91.01, 43.08], [-90.14, 42.59], [-90.15, 41.64], [-90.68, 40.96], [-91.39, 40.56], [-91.51, 40.61], [-91.35, 41.35], [-91.05, 41.93], [-91.14, 42.3], [-91.17, 42.69], [-91.01, 43.08]]]}, "properties": {"objectid": 1, "id": 1, "valid_time": "FEB 28 - MAR 5", "outlook": "Likely", "issue_time": "2017-02-28 19:41:00", "start_time": "2017-02-28 19:41:00", "end_time": "2017-03-05 12:00:00", "st_area(shape)": 1.9917000002878742, "st_length(shape)": 6.359201708649808, "idp_source": "fop", "idp_subset": "default"}})
        
        self.assertEqual(flood.location, {'type': 'Polygon', 'coordinates': [[[-91.01, 43.08], [-90.14, 42.59], [-90.15, 41.64], [-90.68, 40.96], [-91.39, 40.56], [-91.51, 40.61], [-91.35, 41.35], [-91.05, 41.93], [-91.14, 42.3], [-91.17, 42.69], [-91.01, 43.08]]]})
        self.assertEqual(flood.valid_time, "FEB 28 - MAR 5")
        self.assertEqual(flood.outlook, "Likely")
        self.assertEqual(flood.issue_time, datetime(2017, 2, 28, 19, 41, 0))
        self.assertEqual(flood.start_time, datetime(2017, 2, 28, 19, 41, 0))
        self.assertEqual(flood.end_time, datetime(2017, 3, 5, 12, 0, 0))
        self.assertEqual(flood.idp_source, "fop")
        self.assertEqual(flood.idp_subset, "default")

    def test_store_flood_poly(self):
        flood = floods.convert_flood_poly({"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-91.01, 43.08], [-90.14, 42.59], [-90.15, 41.64], [-90.68, 40.96], [-91.39, 40.56], [-91.51, 40.61], [-91.35, 41.35], [-91.05, 41.93], [-91.14, 42.3], [-91.17, 42.69], [-91.01, 43.08]]]}, "properties": {"objectid": 1, "id": 1, "valid_time": "FEB 28 - MAR 5", "outlook": "Likely", "issue_time": "2017-02-28 19:41:00", "start_time": "2017-02-28 19:41:00", "end_time": "2017-03-05 12:00:00", "st_area(shape)": 1.9917000002878742, "st_length(shape)": 6.359201708649808, "idp_source": "fop", "idp_subset": "default"}})
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as db:
                # Ensure flood has been added
                floods.store_flood_poly(db, flood)
                db.execute('SELECT * FROM flood_polys WHERE valid_time = %s', ("FEB 28 - MAR 5",))
                self.assertEqual(db.rowcount, 1)

                # Ensure flood has not been added again
                floods.store_flood_poly(db, flood)
                db.execute('SELECT * FROM flood_polys WHERE valid_time = %s', ("FEB 28 - MAR 5",))
                self.assertEqual(db.rowcount, 1)
