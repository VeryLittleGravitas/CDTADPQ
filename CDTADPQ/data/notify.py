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
            fires = get_all_wild_fires(db)
            for fire in fires:
                user_rows = get_users_to_notify(db, fire)
                for user_row in user_rows:
                    send_notification(twilio_account, user_row['phone_number'], fire)

def get_all_wild_fires(db):
    ''' Return all fires that users should be notified of
    '''
    # Need to not get all fires, need to get all for today or something?
    db.execute('SELECT ST_AsGeoJSON(location) as coordinates_json, * FROM fire_points')
    fire_rows = db.fetchall()
    fires = []
    for fire_row in fire_rows:
        fire_location = json.loads(fire_row['coordinates_json'])
        fire_point = wildfires.FirePoint(fire_location, fire_row['usgs_id'], fire_row['name'],
                                         fire_row['contained'], fire_row['discovered'], fire_row['cause'],
                                         fire_row['acres'])
        fires.append(fire_point)
    return fires

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
    return user_rows

TwilioURL = 'https://api.twilio.com/2010-04-01/Accounts/{account}/Messages.json'

def send_notification(account, to_number, fire):
    ''' Send fire notification to phone number
    '''
    url = uritemplate.expand(TwilioURL, dict(account=account.account))
    body = 'Fire {}'.format(fire.name)
    data = dict(From=account.number, To=to_number, Body=body)
    auth = account.sid, account.secret
    posted = requests.post(url, auth=auth, data=data)
    
    if posted.status_code not in range(200, 299):
        if 'message' in posted.json():
            raise RuntimeError(posted.json()['message'])
        else:
            raise RuntimeError('Bad response from Twilio')
    
    return True


if __name__ == '__main__':
    exit(main())

