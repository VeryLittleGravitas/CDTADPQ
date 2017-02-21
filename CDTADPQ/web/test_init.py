import unittest, os, json, bs4, unittest.mock
from .. import web
from ..data import recreate

class AppTests (unittest.TestCase):

    def setUp(self):
        '''
        '''
        recreate.main(os.environ['DATABASE_URL'])
        self.config = web.app.config
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
    
    def test_register(self):
        '''
        '''
        got = self.client.get('/register')
        self.assertEqual(got.status_code, 200)

        soup = bs4.BeautifulSoup(got.data, 'html.parser')
        form = soup.find('form', id='sign-up')
        data = {input['name']: None for input in form.find_all('input')}
        self.assertIn('phone-number', data)
        data['phone-number'] = '+1 (510) 555-1212'

        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code:
            posted = self.client.open(method=form['method'], path=form['action'], data=data)
            self.assertEqual(posted.status_code, 303)
        
        self.assertEqual(len(send_verification_code.mock_calls), 1)
        self.assertEqual(send_verification_code.mock_calls[0][1][:2],
                         (self.config['twilio_account'], '+1 (510) 555-1212'))
        
        (pin_number, ) = send_verification_code.mock_calls[0][1][2:]
        redirected = self.client.get(posted.headers.get('Location'))
        self.assertEqual(redirected.status_code, 200)

        soup2 = bs4.BeautifulSoup(redirected.data, 'html.parser')
        form2 = soup2.find('form', id='register')
        data2 = {input['name']: None for input in form2.find_all('input')}
        self.assertIn('pin-number', data2)
        data2['pin-number'] = pin_number

        return
        
        confirmed = self.client.open(method=form2['method'], path=form2['action'], data=data2)
        self.assertEqual(confirmed.status_code, 303)
