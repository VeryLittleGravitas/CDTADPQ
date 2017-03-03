import codecs, json, requests, uritemplate
import os, psycopg2, psycopg2.extras

from . import notifications
from . import wildfires
from . import zipcodes
from . import users

def main():
    '''
    '''
    twilio_account = notifications.make_twilio_account(os.environ)
    mailgun_account = notifications.make_mailgun_account(os.environ)

    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as db:
            fires = wildfires.get_current_fires(db)
            for fire in fires:
                users_to_notify = get_users_to_notify(db, fire)
                message = ('Emergency: {}').format(fire.description)
                for user in users_to_notify:
                    send_notification(twilio_account, user, message)
                    send_email_notification(mailgun_account, user, message)
                    log_user_notification(db, user, fire)
                log_notification_for_admin_records(db, message, len(users_to_notify), fire.internal_id, 'fire')

def get_user_locations(db):
    '''
    '''
    db.execute('''SELECT COUNT(u.phone_number) AS users, u.zip_codes[u.index],
                         ST_AsGeoJSON(ST_Centroid(z.geog::geometry)) AS center
                  FROM (
                      SELECT generate_subscripts(zip_codes, 1) AS index, zip_codes, phone_number
                      FROM users
                  ) AS u
                  JOIN tl_2016_us_zcta510 AS z ON z."ZCTA5CE10" = u.zip_codes[u.index]
                  GROUP BY u.zip_codes[u.index], z.geog''')
    
    users = []
    for (count, zip_code, location_geojson) in db.fetchall():
        location = json.loads(location_geojson)
        user = dict(users=count, zip_code=zip_code, location=location)
        users.append(user)
    
    return users

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
    return notifications.send_sms(account, user.phone_number, message)

def send_email_notification(account, user, message):
    ''' Send fire notification to email address
    '''
    if user.email_address:
        return notifications.send_email(account, user.email_address, 'Emergency!', message)

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

