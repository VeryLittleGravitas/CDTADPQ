import unittest, unittest.mock, httmock, urllib.parse
from . import users, notifications

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

    def test_verify_user_signup_good_user(self):
        '''
        '''
        db = unittest.mock.Mock()

        last_execute_args = dict()
        db.execute.side_effect = lambda query, args: last_execute_args.update(query=query, args=args)
        db.fetchone.side_effect = lambda: (
            ('1234', '+15105551212', '94612')
            if last_execute_args['query'].startswith('SELECT pin_number,')
            else None
            )

        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')

        self.assertEqual(verified, '+15105551212')
        self.assertEqual(db.execute.mock_calls[-3][1], ('SELECT pin_number, phone_number, zipcode\n                  FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
        self.assertEqual(db.execute.mock_calls[-2][1], ('SELECT true FROM users WHERE phone_number = %s', ('+15105551212', )))
        self.assertEqual(db.execute.mock_calls[-1][1], ('INSERT INTO users (phone_number, zip_codes) VALUES (%s, %s)', ('+15105551212', ['94612'])))

    def test_verify_user_signup_existing_user(self):
        '''
        '''
        db = unittest.mock.Mock()

        last_execute_args = dict()
        db.execute.side_effect = lambda query, args: last_execute_args.update(query=query, args=args)
        db.fetchone.side_effect = lambda: (
            ('1234', '+15105551212', '94612')
            if last_execute_args['query'].startswith('SELECT pin_number,')
            else [True]
            )

        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')

        self.assertEqual(verified, '+15105551212')
        self.assertEqual(db.execute.mock_calls[-2][1], ('SELECT pin_number, phone_number, zipcode\n                  FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT true FROM users WHERE phone_number = %s', ('+15105551212', )))

    def test_verify_user_signup_no_match(self):
        '''
        '''
        db = unittest.mock.Mock()

        db.fetchone.return_value = None
        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')

        self.assertFalse(verified)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT pin_number, phone_number, zipcode\n                  FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))

    def test_send_verification_code(self):
        '''
        '''
        def response_content_error(url, request):
            if (request.method, url.hostname, url.path) != ('POST', 'api.twilio.com', '/2010-04-01/Accounts/account/Messages.json'):
                raise Exception('Nope')

            if request.headers['Authorization'] != 'Basic c2lkOnNlY3JldA==':
                return httmock.response(401, b'Go away')


            body = 'Your CA Alerts PIN code is 1234. Use this to confirm your phone number. \n\nIf you didn\'t ask for this, please ignore this message.'
            form = dict(urllib.parse.parse_qsl(request.body))

            if form['From'] != 'number':
                return httmock.response(404, b'Not the right number')

            if form == {'From': 'number', 'To': '+15105551212', 'Body': body}:
                body = '''{"sid": "...", "date_created": "Wed, 22 Feb 2017 02:32:26 +0000", "date_updated": "Wed, 22 Feb 2017 02:32:26 +0000", "date_sent": null, "account_sid": "...", "to": "+15105551212", "from": "+15105551212", "messaging_service_sid": null, "body": "Yo", "status": "queued", "num_segments": "1", "num_media": "0", "direction": "outbound-api", "api_version": "2010-04-01", "price": null, "price_unit": "USD", "error_code": null, "error_message": null, "uri": "/2010-04-01/Accounts/.../Messages/....json", "subresource_uris": {"media": "/2010-04-01/Accounts/.../Messages/.../Media.json"}}'''
                return httmock.response(201, body.encode('utf8'), {'Content-Type': 'application/json'})

            if form == {'From': 'number', 'To': '+1212BADCODE', 'Body': body}:
                body = '''{"code": 21211, "message": "The 'To' number is not a valid phone number.", "more_info": "https://www.twilio.com/docs/errors/21211", "status": 400}'''
                return httmock.response(400, body.encode('utf8'), {'Content-Type': 'application/json'})

            raise Exception('Nope')

        account = notifications.TwilioAccount('sid', 'secret', 'account', 'number')

        with httmock.HTTMock(response_content_error):
            users.send_verification_code(account, '+15105551212', '1234')

            with self.assertRaises(RuntimeError) as error:
                users.send_verification_code(account, '+1212BADCODE', '1234')

        self.assertEqual(str(error.exception), "The 'To' number is not a valid phone number.")

    def test_send_email_verification_code(self):
        '''
        '''
        def response_content_error(url, request):
            if (request.method, url.hostname, url.path) != ('POST', 'api.mailgun.net', '/v2/sandbox.mailgun.org/messages'):
                raise Exception('Nope')

            if request.headers['Authorization'] != 'Basic YXBpOnNlY3JldA==':
                return httmock.response(401, b'Go away')

            subj = 'Your CA Alerts PIN code'
            body = 'Your CA Alerts PIN code is 1234.\n\nUse this to confirm your email address. If you didn\'t ask for this, please ignore this message.'

            form = dict(urllib.parse.parse_qsl(request.body))

            if form['from'] != 'disaster-sender':
                return httmock.response(404, b'Not the right sender')

            if form == {'from': 'disaster-sender', 'to': 'disaster-recipient', 'subject': subj, 'text': body}:
                body = '''{"id": "...", "message": "Queued. Thank you."}}'''
                return httmock.response(201, body.encode('utf8'), {'Content-Type': 'application/json'})

            if form == {'from': 'disaster-sender', 'to': 'nobody-special', 'subject': subj, 'text': body}:
                body = '''{"message": "Sandbox subdomains are for test purposes only. Please add your own domain or add the address to authorized recipients in Account Settings."}'''
                return httmock.response(400, body.encode('utf8'), {'Content-Type': 'application/json'})

            raise Exception('Nope')

        account = notifications.MailgunAccount('secret', 'sandbox.mailgun.org', 'disaster-sender')

        with httmock.HTTMock(response_content_error):
            users.send_email_verification_code(account, 'disaster-recipient', '1234')

            with self.assertRaises(RuntimeError) as error:
                users.send_email_verification_code(account, 'nobody-special', '1234')

        self.assertEqual(str(error.exception), "Sandbox subdomains are for test purposes only. Please add your own domain or add the address to authorized recipients in Account Settings.")

    def test_get_user_info(self):
        '''
        '''
        db = unittest.mock.Mock()

        db.fetchone.return_value = ('+1 (510) 555-1212', ['94612'], 'user@example.com', ['non-emergency'])
        user_info = users.get_user_info(db, '+1 (510) 555-1212')

        self.assertEqual(user_info, db.fetchone.return_value)
        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT phone_number, zip_codes, email_address, notification_types\n                  FROM users WHERE phone_number = %s', ('+1 (510) 555-1212',)))

        db.fetchone.return_value = None
        user_info = users.get_user_info(db, '+1 (510) 555-1212')

        self.assertEqual(user_info, db.fetchone.return_value)
        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT phone_number, zip_codes, email_address, notification_types\n                  FROM users WHERE phone_number = %s', ('+1 (510) 555-1212',)))

    def test_update_user_profile(self):
        '''
        '''
        db = unittest.mock.Mock()

        user_info = users.update_user_profile(db, '+1 (510) 555-1212', '94612', 'non-emergency')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('UPDATE users SET zip_codes = %s, notification_types = %s\n                  WHERE phone_number = %s', (['94612'], ['non-emergency'], '+1 (510) 555-1212')))

        user_info = users.update_user_profile(db, '+1 (510) 555-1212', '94612, 94608', '')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('UPDATE users SET zip_codes = %s, notification_types = %s\n                  WHERE phone_number = %s', (['94612', '94608'], [''], '+1 (510) 555-1212')))

        user_info = users.update_user_profile(db, '+1 (510) 555-1212', '94XXX', 'non-emergency')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('UPDATE users SET zip_codes = %s, notification_types = %s\n                  WHERE phone_number = %s', ([], ['non-emergency'], '+1 (510) 555-1212')))

    def test_delete_user(self):
        '''
        '''
        db = unittest.mock.Mock()

        users.delete_user(db, '+1 (510) 555-1212')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('DELETE FROM users WHERE phone_number = %s', ('+1 (510) 555-1212',)))

    def test_get_all_users(self):
        '''
        '''
        db = unittest.mock.Mock()
        db.fetchall.return_value = [dict(id=1, phone_number='+15105551212', zip_codes=['94103'],
                                         email_address='me@example.com', emergency_types=['fire'])]

        users.get_all_users(db, '')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT * FROM users',))

        users.get_all_users(db, 'non-emergency')

        self.assertEqual(db.execute.mock_calls[-1][1],
                         ('SELECT * FROM users WHERE %s = ANY(notification_types)', ('non-emergency', )))
