import unittest, os, unittest.mock as mock
from datetime import datetime
import psycopg2

from . import recreate
from . import earthquakes

class EarthquakeTests (unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.database_url = os.environ['DATABASE_URL']
        recreate.main(self.database_url)

    
    def test_main(self):
        with mock.patch('CDTADPQ.data.sources.load_esri_source') as load_esri_source:
            earthquakes.main()
        
        load_esri_source.assert_called_once_with('http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/Earthquakes/EarthquakesFromLastSevenDays/MapServer/0')
    
    def test_convert_quake_point(self):
        quake = earthquakes.convert_quake_point({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-116.8933333, 32.77466670000007]},  'properties': {"objectid": 273461806, "datetime": 1440702216000, "depth": None, "eqid": "ci37234359", "latitude": -116.8933333, "longitude": 32.7746667, "magnitude": 1.33, "numstations": 17, "region": "5km NE of Rancho San Diego, California", "source": ",ci,", "version": None}})
        
        self.assertEqual(quake.location, {'type': 'Point', 'coordinates': [-116.8933333, 32.77466670000007]})
        self.assertEqual(quake.quake_id, 'ci37234359')
        self.assertEqual(quake.magnitude, 1.33)
        self.assertEqual(quake.depth, None)
        self.assertEqual(quake.numstations, 17)
        self.assertEqual(quake.region, "5km NE of Rancho San Diego, California")
        self.assertEqual(quake.datetime, datetime(2015, 8, 27, 19, 3, 36))
