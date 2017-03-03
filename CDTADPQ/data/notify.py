import codecs, json, requests, uritemplate
import os, psycopg2, psycopg2.extras


from . import wildfires
from . import zipcodes
from . import users

def main():
    '''
    '''
    if os.environ['TWILIO_ACCOUNT'].startswith('AC'):
        # TODO move TwilioAccount out of users
        twilio_account = users.TwilioAccount(
            sid = os.environ.get('TWILIO_SID', ''),
            secret = os.environ.get('TWILIO_SECRET', ''),
            account = os.environ.get('TWILIO_ACCOUNT', ''),
            number = os.environ.get('TWILIO_NUMBER', '')
            )
    else:
        twilio_account = users.TwilioAccount(
            sid = codecs.decode(os.environ.get('TWILIO_SID', ''), 'rot13'),
            secret = codecs.decode(os.environ.get('TWILIO_SECRET', ''), 'rot13'),
            account = codecs.decode(os.environ.get('TWILIO_ACCOUNT', ''), 'rot13'),
            number = os.environ.get('TWILIO_NUMBER', '')
            )

    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as db:
            fires = wildfires.get_current_fires(db)
            for fire in fires:
                users_to_notify = get_users_to_notify(db, fire)
                message = ('Emergency: {}').format(fire.description)
                for user in users_to_notify:
                    send_notification(twilio_account, user, message)
                    log_user_notification(db, user, fire)
                log_notification_for_admin_records(db, message, len(users_to_notify), fire.internal_id, 'fire')

def get_users_to_notify(db, fire_point):
    ''' Return the users that should be notified of this fire
    '''
    radius_meters = float(os.environ.get('RADIUS_MILES', 50)) * 1609.34

    # Convert input GeoJSON to WKT
    fire_json = json.dumps(fire_point.location)
    db.execute('SELECT ST_AsText(ST_GeomFromGeoJSON(%s))', (fire_json, ))
    (geography_wkt, ) = db.fetchone()
    
    db.execute('''SELECT DISTINCT users.*
                  FROM users
                  JOIN (
                      SELECT "ZCTA5CE10" AS zip_code
                      FROM tl_2016_us_zcta510
                      WHERE ST_Intersects(geog, ST_Buffer(ST_GeographyFromText(%s), %s))
                  ) AS zip_codes
                  ON zip_codes.zip_code = ANY (users.zip_codes)''',
               (geography_wkt, radius_meters))

    user_rows = db.fetchall()

    # Filter out users that shouldn't be notified
    users_to_notify = []
    for user_row in user_rows:
        db.execute('SELECT * FROM user_emergencies_log WHERE user_id = %s AND emergency_external_id = %s AND emergency_type = %s LIMIT 1',
                   (user_row['id'], fire_point.usgs_id, 'fire'))
        user_has_been_notified = db.rowcount
        if not user_has_been_notified:
            users_to_notify.append(users.User(user_row['id'], user_row['phone_number'], user_row['zip_codes'],
                                              user_row['email_address'], user_row['emergency_types']))
    return users_to_notify

TwilioURL = 'https://api.twilio.com/2010-04-01/Accounts/{account}/Messages.json'

def send_notification(account, user, message):
    ''' Send fire notification to phone number
    '''
    url = uritemplate.expand(TwilioURL, dict(account=account.account))
    data = dict(From=account.number, To=user.phone_number, Body=message)
    auth = account.sid, account.secret
    posted = requests.post(url, auth=auth, data=data)
    
    if posted.status_code not in range(200, 299):
        if 'message' in posted.json():
            raise RuntimeError(posted.json()['message'])
        else:
            raise RuntimeError('Bad response from Twilio')
    return True

def log_user_notification(db, user, fire):
    ''' Log that the user has been notified of this emergency
    '''
    db.execute('INSERT INTO user_emergencies_log (emergency_type, emergency_external_id, user_id) VALUES (%s, %s, %s)',
                ('fire', fire.usgs_id, user.id))
    return True

def log_notification_for_admin_records(db, message, notified_users_count, emergency_id=None, emergency_type=None):
    ''' Log the notification so admins can see notifications previously sent
    '''
    db.execute('INSERT INTO notifications_log (message, notified_users_count, emergency_id, emergency_type) VALUES (%s, %s, %s, %s)',
                (message, notified_users_count, emergency_id, emergency_type))
    return True

if __name__ == '__main__':
    exit(main())

