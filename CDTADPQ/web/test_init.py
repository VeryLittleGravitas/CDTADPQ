import unittest, os, psycopg2, json
from .. import web

class AppTests (unittest.TestCase):

    def setUp(self):
        '''
        '''
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'app.pgsql')) as file:
            with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
                with conn.cursor() as db:
                    db.execute(file.read())

        self.client = web.app.test_client()
    
    def test_index(self):
        '''
        '''
        got = self.client.get('/')
        html = got.data.decode('utf8')
        self.assertIn('<link rel="stylesheet" href="/static/uswds-0.14.0/css/uswds.min.css">', html)
        self.assertIn('<script src="/static/uswds-0.14.0/js/uswds.min.js">', html)
    
    def test_earth(self):
        '''
        '''
        got = self.client.get('/earth.geojson')
        geojson = json.loads(got.data.decode('utf8'))
        self.assertEqual({"type": "FeatureCollection", "features": [{"geometry": {"coordinates": [[[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]], "type": "Polygon"}, "properties": {}, "type": "Feature"}]}, geojson)
