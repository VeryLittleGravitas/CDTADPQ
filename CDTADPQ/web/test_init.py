import unittest, os, json, bs4, unittest.mock
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
        self.assertIn('<link rel="stylesheet" href="/static/uswds-0.14.0/css/uswds.min.css">', html)
        self.assertIn('<script src="/static/uswds-0.14.0/js/uswds.min.js">', html)
    
    def test_earth(self):
        '''
        '''
        got = self.client.get('/earth.geojson')
        geojson = json.loads(got.data.decode('utf8'))
        self.assertEqual({"type": "FeatureCollection", "features": [{"geometry": {"coordinates": [[[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]], "type": "Polygon"}, "properties": {}, "type": "Feature"}]}, geojson)
    
    def test_signup(self):
        '''
        '''
        got = self.client.get('/register')
        self.assertEqual(got.status_code, 200)

        soup = bs4.BeautifulSoup(got.data, 'html.parser')
        form = soup.find('form', id='sign-up')
        data = {input['name']: None for input in form.find_all('input')}
        self.assertIn('phone-number', data)
        data['phone-number'] = '+1 (510) 555-1212'

        with unittest.mock.patch('CDTADPQ.data.users.add_verified_signup') as add_verified_signup:
            posted = self.client.open(method=form['method'], path=form['action'], data=data)
            self.assertEqual(posted.status_code, 200)
        
        self.assertEqual(len(add_verified_signup.mock_calls), 1)
        self.assertEqual(add_verified_signup.mock_calls[0][1][1:], ('+1 (510) 555-1212', ))
