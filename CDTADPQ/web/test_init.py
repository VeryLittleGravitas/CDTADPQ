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
        # Start at the front page and look for a registration link

        got1 = self.client.get('/')
        self.assertEqual(got1.status_code, 200)
        
        soup1 = bs4.BeautifulSoup(got1.data, 'html.parser')
        link1 = soup1.find(text='Register').find_parent('a')
        
        # Get the registration form

        got2 = self.client.get(link1['href'])
        self.assertEqual(got2.status_code, 200)

        soup2 = bs4.BeautifulSoup(got2.data, 'html.parser')
        form2 = soup2.find('form', id='sign-up')
        data2 = {input['name']: None for input in form2.find_all('input')}
        self.assertIn('phone-number', data2)
        data2['phone-number'] = '+1 (510) 555-1212'

        # Enter phone number to register

        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code:
            posted1 = self.client.open(method=form2['method'], path=form2['action'], data=data2)
            self.assertEqual(posted1.status_code, 303)
        
        self.assertEqual(len(send_verification_code.mock_calls), 1)
        self.assertEqual(send_verification_code.mock_calls[0][1][:2],
                         (self.config['twilio_account'], '+1 (510) 555-1212'))
        
        (pin_number, ) = send_verification_code.mock_calls[0][1][2:]

        # Follow redirect for PIN confirmation

        got3 = self.client.get(posted1.headers.get('Location'))
        self.assertEqual(got3.status_code, 200)

        soup3 = bs4.BeautifulSoup(got3.data, 'html.parser')
        form3 = soup3.find('form', id='register')
        data3 = {input['name']: input.get('value') for input in form3.find_all('input')}
        self.assertIn('pin-number', data3)
        data3['pin-number'] = pin_number
        
        # Enter the PIN number to confirm

        posted2 = self.client.open(method=form3['method'], path=form3['action'], data=data3)
        self.assertEqual(posted2.status_code, 303)

        # Follow redirect after PIN confirmation

        got4 = self.client.get(posted2.headers.get('Location'))
        self.assertEqual(got4.status_code, 200)
        
        soup4 = bs4.BeautifulSoup(got4.data, 'html.parser')
        text4 = soup4.find(text='Profile')
        self.assertIsNotNone(text4)

        link4 = text4.find_parent('a')
        self.assertIn(link4['href'], posted2.headers.get('Location'))

        form4 = soup4.find('form', id='log-out')
        data4 = {input['name']: input.get('value') for input in form4.find_all('input')}

        # Log out using the form

        posted3 = self.client.open(method=form4['method'], path=form4['action'], data=data4)
        self.assertEqual(posted3.status_code, 303)

        # Follow the redirect to the front page

        got5 = self.client.get(posted3.headers.get('Location'))
        self.assertEqual(got5.status_code, 200)

        # Try that post-confirmation profile page again - are we logged out?

        got6 = self.client.get(posted2.headers.get('Location'))
        self.assertEqual(got6.status_code, 401)
