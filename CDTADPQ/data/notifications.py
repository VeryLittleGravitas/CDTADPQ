import uritemplate, requests, codecs

TwilioURL = 'https://api.twilio.com/2010-04-01/Accounts/{account}/Messages.json'
MailgunURL = 'https://api.mailgun.net/v2/{domain}/messages'

class MailgunAccount:

    def __init__(self, api_key, domain, sender):
        self.api_key = api_key
        self.domain = domain
        self.sender = sender

class TwilioAccount:

    def __init__(self, sid, secret, account, number):
        self.sid = sid
        self.secret = secret
        self.account = account
        self.number = number

def make_twilio_account(environ):
    '''
    '''
    if environ['TWILIO_ACCOUNT'].startswith('AC'):
        return TwilioAccount(
            sid = environ.get('TWILIO_SID', ''),
            secret = environ.get('TWILIO_SECRET', ''),
            account = environ.get('TWILIO_ACCOUNT', ''),
            number = environ.get('TWILIO_NUMBER', '')
            )
    else:
        return TwilioAccount(
            sid = codecs.decode(environ.get('TWILIO_SID', ''), 'rot13'),
            secret = codecs.decode(environ.get('TWILIO_SECRET', ''), 'rot13'),
            account = codecs.decode(environ.get('TWILIO_ACCOUNT', ''), 'rot13'),
            number = environ.get('TWILIO_NUMBER', '')
            )

def make_mailgun_account(environ):
    '''
    '''

    return MailgunAccount(
        api_key = environ.get('MAILGUN_API_KEY', ''),
        domain = environ.get('MAILGUN_DOMAIN', ''),
        sender = environ.get('MAILGUN_SENDER', 'alerts@verylittlegravitas.com')
        )

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

def send_email(account, email_address, subject, body):
    '''
    '''
    url = uritemplate.expand(MailgunURL, dict(domain=account.domain))
    data = {'from': account.sender, 'to': email_address, 'subject': subject, 'text': body}
    auth = 'api', account.api_key
    posted = requests.post(url, auth=auth, data=data)

    if posted.status_code not in range(200, 299):
        if 'message' in posted.json():
            raise RuntimeError(posted.json()['message'])
        else:
            raise RuntimeError('Bad response from Mailgun')

    return True
