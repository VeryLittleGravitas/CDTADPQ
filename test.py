import unittest, os, psycopg2, json
from app import app

class AppTests (unittest.TestCase):

    def setUp(self):
        '''
        '''
        with open(os.path.join(os.path.dirname(__file__), 'app.pgsql')) as file:
            with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
                with conn.cursor() as db:
                    db.execute(file.read())

        self.client = app.test_client()
    
    def test_app(self):
        '''
        '''
        got = self.client.get('/')
        geojson = json.loads(got.data.decode('utf8'))
        self.assertEqual({"type": "FeatureCollection", "features": [{"geometry": {"coordinates": [[[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]], "type": "Polygon"}, "properties": {}, "type": "Feature"}]}, geojson)

if __name__ == '__main__':
    unittest.main()
