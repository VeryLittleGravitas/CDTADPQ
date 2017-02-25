import unittest, unittest.mock, httmock, urllib.parse
from . import users

class UsersTests (unittest.TestCase):

    def test_add_unverified_signup(self):
        '''
        '''
        db, account = unittest.mock.Mock(), unittest.mock.Mock()
        to_number, signup_id = '+1 (510) 555-1212', 'xxx-yy-zzz'
        zipcode, pin_number = '94612', 1234
        
        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code, \
             unittest.mock.patch('random.randint') as randint, \
             unittest.mock.patch('uuid.uuid4') as uuid4:
            randint.return_value = pin_number
            uuid4.return_value = signup_id
            output_id = users.add_unverified_signup(db, account, to_number, zipcode)
        
        self.assertEqual(output_id, signup_id)
        
        db.execute.assert_called_once_with(
            '''INSERT INTO unverified_signups
                  (signup_id, phone_number, pin_number, zipcode)
                  VALUES (%s, %s, %s, %s)''',
               (signup_id, to_number, str(pin_number), zipcode))
        
        send_verification_code.assert_called_once_with(account, to_number, str(pin_number))
    
    def test_verify_user_signup(self):
        '''
        '''
        db = unittest.mock.Mock()
        
        db.fetchone.return_value = ('1234', '+15105551212')
        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')
        
        self.assertEqual(verified, '+15105551212')
        self.assertEqual(db.execute.mock_calls[-2][1], ('SELECT pin_number, phone_number FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
        self.assertEqual(db.execute.mock_calls[-1][1], ('INSERT INTO users (phone_number) VALUES (%s)', ('+15105551212',)))
        
        db.fetchone.return_value = None
        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')
        
        self.assertFalse(verified)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT pin_number, phone_number FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
    
    def test_send_verification_code(self):
        '''
        '''
        def response_content_error(url, request):
            if (request.method, url.hostname, url.path) != ('POST', 'api.twilio.com', '/2010-04-01/Accounts/account/Messages.json'):
                raise Exception('Nope')

            if request.headers['Authorization'] != 'Basic c2lkOnNlY3JldA==':
                return httmock.response(401, b'Go away')
            
            form = dict(urllib.parse.parse_qsl(request.body))
            
            if form['From'] != 'number':
                return httmock.response(404, b'Not the right number')

            if form == {'From': 'number', 'To': '+15105551212', 'Body': 'Yo 1234'}:
                body = '''{"sid": "...", "date_created": "Wed, 22 Feb 2017 02:32:26 +0000", "date_updated": "Wed, 22 Feb 2017 02:32:26 +0000", "date_sent": null, "account_sid": "...", "to": "+15105551212", "from": "+15105551212", "messaging_service_sid": null, "body": "Yo", "status": "queued", "num_segments": "1", "num_media": "0", "direction": "outbound-api", "api_version": "2010-04-01", "price": null, "price_unit": "USD", "error_code": null, "error_message": null, "uri": "/2010-04-01/Accounts/.../Messages/....json", "subresource_uris": {"media": "/2010-04-01/Accounts/.../Messages/.../Media.json"}}'''
                return httmock.response(201, body.encode('utf8'), {'Content-Type': 'application/json'})

            if form == {'From': 'number', 'To': '+1212BADCODE', 'Body': 'Yo 1234'}:
                body = '''{"code": 21211, "message": "The 'To' number is not a valid phone number.", "more_info": "https://www.twilio.com/docs/errors/21211", "status": 400}'''
                return httmock.response(400, body.encode('utf8'), {'Content-Type': 'application/json'})

            raise Exception('Nope')
        
        account = users.TwilioAccount('sid', 'secret', 'account', 'number')
        
        with httmock.HTTMock(response_content_error):
            users.send_verification_code(account, '+15105551212', '1234')

            with self.assertRaises(RuntimeError) as error:
                users.send_verification_code(account, '+1212BADCODE', '1234')

        self.assertEqual(str(error.exception), "The 'To' number is not a valid phone number.")
    
    def test_get_user_info(self):
        '''
        '''
        db = unittest.mock.Mock()
        
        db.fetchone.return_value = ('+1 (510) 555-1212', ['94612'])
        user_info = users.get_user_info(db, '+1 (510) 555-1212')

        self.assertEqual(user_info, db.fetchone.return_value)
        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT phone_number, zip_codes FROM users WHERE phone_number = %s', ('+1 (510) 555-1212',)))
        
        db.fetchone.return_value = None
        user_info = users.get_user_info(db, '+1 (510) 555-1212')

        self.assertEqual(user_info, db.fetchone.return_value)
        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT phone_number, zip_codes FROM users WHERE phone_number = %s', ('+1 (510) 555-1212',)))
