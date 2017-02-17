import unittest, unittest.mock as mock
from datetime import datetime

from . import wildfires

class WildfireTests (unittest.TestCase):
    
    def test_main(self):
        with mock.patch('CDTADPQ.data.sources.load_esri_source') as load_esri_source:
            wildfires.main()
        
        load_esri_source.assert_called_once_with('https://wildfire.cr.usgs.gov/arcgis/rest/services/geomac_fires/MapServer/1')
    
    def test_convert_fire_point(self):
        fire = wildfires.convert_fire_point({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-95.0780629, 35.7197286]}, 'properties': {'objectid': 1, 'latitude': 35.7197, 'longitude': -95.0781, 'gacc': 'SACC', 'hotlink': 'http://www.nifc.gov/fireInfo/nfn.htm', 'state': 'OK', 'status': 'I', 'irwinid': '{14DD44C2-ACF0-4998-A99B-971BF60E9A11}', 'acres': 1500, 'firecause': 'Human', 'reportdatetime': 1487091600000, 'percentcontained': 49, 'uniquefireidentifier': '2017-OKNEU-170102', 'firediscoverydatetime': 1486984500000, 'complexparentirwinid': None, 'pooresponsibleunit': 'OKNEU', 'incidentname': 'Spike Road', 'iscomplex': 'false', 'irwinmodifiedon': 1487067267000, 'mapsymbol': '1', 'datecurrent': 1487235965000, 'pooownerunit': None, 'owneragency': None, 'fireyear': None, 'localincidentidentifier': None, 'incidenttypecategory': None}})
        
        self.assertEqual(fire.geometry, {'type': 'Point', 'coordinates': [-95.0780629, 35.7197286]})
        self.assertEqual(fire.unique_id, '2017-OKNEU-170102')
        self.assertEqual(fire.fire_name, 'Spike Road')
        self.assertEqual(fire.contained, 49)
        self.assertEqual(fire.discovered, datetime(2017, 2, 13, 11, 15))
        self.assertEqual(fire.cause, 'Human')
        self.assertEqual(fire.acres, 1500)
