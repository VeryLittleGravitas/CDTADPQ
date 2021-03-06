import flask, codecs, psycopg2, os, json, functools, sys, itsdangerous, psycopg2.extras
from ..data import users, zipcodes, wildfires, notify, earthquakes, floods, stats, notifications

def user_is_logged_in(untouched_route):
    ''' Checks for presence of "phone_number" session variable.
    '''
    @functools.wraps(untouched_route)
    def wrapper(*args, **kwargs):
        if 'phone_number' not in flask.session:
            body = flask.render_template('error-auth.html', **template_kwargs())
            return flask.Response(body, status=401)

        return untouched_route(*args, **kwargs)
    
    return wrapper

def user_is_an_admin(untouched_route):
    ''' Checks for presence of admin username and password.
    '''
    @functools.wraps(untouched_route)
    def wrapper(*args, **kwargs):
        expected_auth = flask.current_app.config['admin_credentials']
        if flask.request.authorization != expected_auth:
            body = flask.render_template('error-auth.html', **template_kwargs())
            head = {'WWW-Authenticate': 'Basic realm="California Emergency Alerts admin area"'}
            return flask.Response(body, status=401, headers=head)

        return untouched_route(*args, **kwargs)
    
    return wrapper

def template_kwargs():
    '''
    '''
    return dict(
        user_is_logged_in = bool('phone_number' in flask.session)
        )

def emergencies2geojson(emergencies, include_hrefs):
    '''
    '''
    features = [
        dict(
            type='Feature',
            geometry=e.location,
            properties=dict(
                type=e.type,
                id=e.id,
                title=e.title,
                description=e.description,
                href=(flask.url_for('get_send_alert', type=e.type, id=e.id) if include_hrefs else None)
                ))
        for e in emergencies
        ]
    
    return dict(type='FeatureCollection', features=features)

def users2geojson(users):
    '''
    '''
    features = [
        dict(
            type='Feature',
            geometry=u['location'],
            properties=dict(
                users=u['users'],
                zip_code=u['zip_code']
                ))
        for u in users
        ]
    
    return dict(type='FeatureCollection', features=features)

app = flask.Flask(__name__) 
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.config['twilio_account'] = notifications.make_twilio_account(os.environ)
app.config['mailgun_account'] = notifications.make_mailgun_account(os.environ)

app.config['admin_credentials'] = dict(
    username = os.environ.get('ADMIN_USERNAME', 'admin'),
    password = os.environ.get('ADMIN_PASSWORD', 'admin'),
    )

@app.route('/')
def get_index():
    emergencies = list()
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            emergencies.extend(earthquakes.get_current_quakes(db))
            emergencies.extend(wildfires.get_current_fires(db))
            emergencies.extend(floods.get_current_floods(db))
    
    emergencies_geojson = emergencies2geojson(emergencies, False)
    return flask.render_template('index.html', emergencies_geojson=emergencies_geojson,
                                 **template_kwargs())

@app.route('/about')
def get_about():
    return flask.render_template('about.html', **template_kwargs())

@app.route('/logout', methods=['POST'])
@user_is_logged_in
def post_logout():
    flask.session.pop('phone_number')
    if 'is_registering' in flask.session:
        flask.session.pop('is_registering')
    return flask.redirect(flask.url_for('get_index'), code=303)

@app.route('/register', methods=['GET'])
def get_register():
    flask.session['is_registering'] = 1
    return flask.render_template('register.html', **template_kwargs())

@app.route('/login', methods=['GET'])
def get_login():
    return flask.render_template('login.html')

@app.route('/register', methods=['POST'])
def post_register():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            twilio_account = flask.current_app.config['twilio_account']
            to_number = flask.request.form['phone-number']
            zipcode = flask.request.form.get('zipcode', None)
            signup_id = users.add_unverified_signup(db, twilio_account, to_number, zipcode)
            return flask.redirect(flask.url_for('get_registered', signup_id=signup_id), code=303)

@app.route('/registered/<signup_id>')
def get_registered(signup_id):
    return flask.render_template('registered.html', signup_id=signup_id)

@app.route('/confirm', methods=['POST'])
def post_confirm():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            pin_number = flask.request.form['pin-number']
            signup_id = flask.request.form['signup-id']
            phone_number = users.verify_user_signup(db, pin_number, signup_id)
            
            if phone_number is False:
                body = flask.render_template('registered.html', signup_id=signup_id,
                                             error_wrong_pin_number=True)
                return flask.Response(body, status=400)
            
            flask.session['phone_number'] = phone_number

            if 'is_registering' in flask.session:
                return flask.redirect(flask.url_for('get_confirmation'), code=303)
            else:
                return flask.redirect(flask.url_for('get_profile'), code=303)

@app.route('/api/')
def get_api():
    return flask.render_template('api-index.html', **template_kwargs())

@app.route('/api/zipcode')
def get_zipcode():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            lat, lon = [float(flask.request.args[k]) for k in ('lat', 'lon')]
            zipcode = zipcodes.lookup_zipcode(db, lat, lon)
            
    if zipcode is None:
        return flask.jsonify({})
    else:
        return flask.jsonify({'zipcode': zipcode})

@app.route('/confirmation')
@user_is_logged_in
def get_confirmation():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            phone_number, zip_codes, email_address, notification_types \
                = users.get_user_info(db, flask.session['phone_number'])
        
    zip_code_str = ', '.join(zip_codes) if zip_codes else ''
    email_addr_str = email_address or ''
    return flask.render_template('confirmation.html', phone_number=phone_number,
                                 zip_codes=zip_code_str, email_address=email_addr_str,
                                 **template_kwargs())

@app.route('/profile', methods=['GET'])
@user_is_logged_in
def get_profile():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            phone_number, zip_codes, email_address, notification_types \
                = users.get_user_info(db, flask.session['phone_number'])
        
    zip_code_str = ', '.join(zip_codes) if zip_codes else ''
    email_addr_str = email_address or ''
    is_checked = 'checked' if notification_types and 'non-emergency' in notification_types else ''
    return flask.render_template('profile.html', phone_number=phone_number,
                                 zip_codes=zip_code_str, email_address=email_addr_str, is_checked=is_checked,
                                 **template_kwargs())

@app.route('/profile', methods=['POST'])
@user_is_logged_in
def post_profile():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            if flask.request.form.get('action') == 'Delete Profile':
                users.delete_user(db, flask.session['phone_number'])
                flask.session.pop('phone_number')
                if 'is_registering' in flask.session:
                    flask.session.pop('is_registering')
                return flask.redirect(flask.url_for('get_register'), code=303)

            else:
                phone_number = flask.session['phone_number']
                zip_codes_str = flask.request.form.get('zip-codes', '')
                notification_type_str = flask.request.form.get('non-emergencies', '')
                users.update_user_profile(db, phone_number, zip_codes_str, notification_type_str)
                redirect_url = flask.url_for('get_profile')
                return flask.redirect(redirect_url, code=303)

@app.route('/profile/email-address', methods=['POST'])
@user_is_logged_in
def post_email_address():
    email_address = flask.request.form['email-address']
    users.send_email_verification_code(app.config['mailgun_account'], email_address, 1234)

    signer = itsdangerous.URLSafeSerializer(flask.current_app.secret_key)
    address_encoded = signer.dumps(email_address)
    redirect_url = flask.url_for('get_email_addressed', address_encoded=address_encoded)

    return flask.redirect(redirect_url, code=303)

@app.route('/profile/email-addressed/<address_encoded>', methods=['GET'])
@user_is_logged_in
def get_email_addressed(address_encoded):
    signer = itsdangerous.URLSafeSerializer(flask.current_app.secret_key)
    email_address = signer.loads(address_encoded)
    print('TEST', email_address, 'from', address_encoded)
    return flask.render_template('email-registered.html', email_address=email_address)
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            phone_number = flask.session['phone_number']
            users.update_email_address(db, phone_number, email_address)

@app.route('/profile/email-confirm', methods=['POST'])
@user_is_logged_in
def post_email_confirm():
    print(flask.request.form)
    pin_number = flask.request.form['pin-number']
    if pin_number != '1234':
        return 'WRONG NUMBER'
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            phone_number = flask.session['phone_number']
            email_address = flask.request.form['email-address']
            users.update_email_address(db, phone_number, email_address)
    return flask.redirect(flask.url_for('get_profile'), code=303)


@app.route('/admin/')
@user_is_an_admin
def get_admin():
    emergencies = list()
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            emergencies.extend(earthquakes.get_current_quakes(db))
            emergencies.extend(wildfires.get_current_fires(db))
            emergencies.extend(floods.get_current_floods(db))
            users = notify.get_user_locations(db)
    
    emergencies_geojson = emergencies2geojson(emergencies, True)
    users_geojson = users2geojson(users)
    return flask.render_template('admin.html', emergencies=emergencies,
                                 emergencies_geojson=emergencies_geojson,
                                 users_geojson=users_geojson, **template_kwargs())

@app.route('/admin/send-alert/<type>/<id>')
@user_is_an_admin
def get_send_alert(type, id):
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            if type == 'fire':
                emergency = wildfires.get_one_fire(db, id)
            if type == 'flood':
                emergency = floods.get_one_flood(db, id)
    return flask.render_template('send-alert.html', emergency=emergency,
                                 **template_kwargs())

@app.route('/admin/send-alert', methods=['POST'])
@user_is_an_admin
def post_send_alert():
    type = flask.request.form['emergency-type']
    id = flask.request.form['emergency-id']
    message = flask.request.form['emergency-message']
    twilio_account = flask.current_app.config['twilio_account']
    mailgun_account = flask.current_app.config['mailgun_account']
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            if type == 'fire':
                emergency = wildfires.get_one_fire(db, id)
            elif type == 'flood':
                emergency = floods.get_one_flood(db, id)
            else:
                emergency = None
            if emergency:
                users_to_notify = notify.get_users_to_notify(db, emergency)
                for user in users_to_notify:
                    print('notify.send_notification:', user, message)
                    notify.send_notification(twilio_account, user, message)
                    notify.send_email_notification(mailgun_account, user, message)
                    notify.log_user_notification(db, user, emergency)
                notify.log_notification_for_admin_records(db, message, len(users_to_notify), emergency.internal_id, 'fire')
    return flask.redirect(flask.url_for('get_sent_alert'), code=303)

@app.route('/admin/sent')
@user_is_an_admin
def get_sent_alert():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            statistics = stats.get_all_notifications_log_rows(db)
    return flask.render_template('sent.html', statistics=statistics, **template_kwargs())

@app.route('/admin/log', methods=['GET'])
def get_log():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            statistics = stats.get_all_notifications_log_rows(db)
    return flask.render_template('admin-sent.html', statistics=statistics,
                                 **template_kwargs())

@app.route('/admin/send-broadcast-alert', methods=['POST'])
@user_is_an_admin
def post_send_broadcast_alert():
    message = flask.request.form['emergency-message']
    notification_type = flask.request.form['broadcast-notification-types']
    twilio_account = flask.current_app.config['twilio_account']
    mailgun_account = flask.current_app.config['mailgun_account']
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            users_to_notify = users.get_all_users(db, notification_type)
            for user in users_to_notify:
                print('notify.send_notification:', user, message)
                notify.send_notification(twilio_account, user, message)
                notify.send_email_notification(mailgun_account, user, message)
            notify.log_notification_for_admin_records(db, message, len(users_to_notify))
    return flask.redirect(flask.url_for('get_sent_alert'), code=303)

@app.route('/stats')
def get_stats():
    return flask.render_template('stats.html', **template_kwargs())
