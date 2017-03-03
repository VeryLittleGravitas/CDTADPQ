import unittest, httmock, urllib.parse

from . import notifications

class NotificationsTests (unittest.TestCase):

    def test_send_sms(self):
        '''
        '''
        account = notifications.TwilioAccount('sid', 'secret', 'account', 'number')
        fire = unittest.mock.Mock(name='Bad Fire')

        def response_content_error(url, request):
            if (request.method, url.hostname, url.path) != ('POST', 'api.twilio.com', '/2010-04-01/Accounts/account/Messages.json'):
                raise Exception('Nope')

            if request.headers['Authorization'] != 'Basic c2lkOnNlY3JldA==':
                return httmock.response(401, b'Go away')
            
            form = dict(urllib.parse.parse_qsl(request.body))
            
            if form == {'From': 'number', 'To': '+15105551212', 'Body': 'omg fire'}:
                body = '''{"sid": "...", "date_created": "Wed, 22 Feb 2017 02:32:26 +0000", "date_updated": "Wed, 22 Feb 2017 02:32:26 +0000", "date_sent": null, "account_sid": "...", "to": "+15105551212", "from": "+15105551212", "messaging_service_sid": null, "body": "Yo", "status": "queued", "num_segments": "1", "num_media": "0", "direction": "outbound-api", "api_version": "2010-04-01", "price": null, "price_unit": "USD", "error_code": null, "error_message": null, "uri": "/2010-04-01/Accounts/.../Messages/....json", "subresource_uris": {"media": "/2010-04-01/Accounts/.../Messages/.../Media.json"}}'''
                return httmock.response(201, body.encode('utf8'), {'Content-Type': 'application/json'})

            raise Exception('Nope')
        
        with httmock.HTTMock(response_content_error):
            notifications.send_sms(account, '+15105551212', 'omg fire')
