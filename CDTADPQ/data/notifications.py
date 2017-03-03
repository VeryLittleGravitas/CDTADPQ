import uritemplate, requests

TwilioURL = 'https://api.twilio.com/2010-04-01/Accounts/{account}/Messages.json'

class TwilioAccount:

    def __init__(self, sid, secret, account, number):
        self.sid = sid
        self.secret = secret
        self.account = account
        self.number = number

def send_sms(account, to_number, body):
    '''
    '''
    url = uritemplate.expand(TwilioURL, dict(account=account.account))
    data = dict(From=account.number, To=to_number, Body=body)
    auth = account.sid, account.secret
    posted = requests.post(url, auth=auth, data=data)

    if posted.status_code not in range(200, 299):
        if 'message' in posted.json():
            raise RuntimeError(posted.json()['message'])
        else:
            raise RuntimeError('Bad response from Twilio')

    return True
