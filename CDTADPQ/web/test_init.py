import unittest, os, json
from .. import web
from ..data import recreate

class AppTests (unittest.TestCase):

    def setUp(self):
        '''
        '''
        recreate.main(os.environ['DATABASE_URL'])
        self.client = web.app.test_client()
    
    def test_index(self):
        '''
        '''
        got = self.client.get('/')
        html = got.data.decode('utf8')
        self.assertIn('Very Little Gravitas', html)
        self.assertIn('Yo, A Page', html)
        self.assertIn('Yo, Page Title', html)
        self.assertIn('<link rel="stylesheet" href="/static/uswds-0.14.0/css/uswds.min.css">', html)
        self.assertIn('<script src="/static/uswds-0.14.0/js/uswds.min.js">', html)
    
    def test_earth(self):
        '''
        '''
        got = self.client.get('/earth.geojson')
        geojson = json.loads(got.data.decode('utf8'))
        self.assertEqual({"type": "FeatureCollection", "features": [{"geometry": {"coordinates": [[[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]], "type": "Polygon"}, "properties": {}, "type": "Feature"}]}, geojson)
