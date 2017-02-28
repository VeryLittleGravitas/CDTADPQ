import flask, codecs, psycopg2, os, json, functools, sys, itsdangerous, psycopg2.extras
from ..data import users, zipcodes, wildfires, notify

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

app = flask.Flask(__name__) 
app.secret_key = os.environ['FLASK_SECRET_KEY']

if os.environ['TWILIO_ACCOUNT'].startswith('AC'):
    app.config['twilio_account'] = users.TwilioAccount(
        sid = os.environ.get('TWILIO_SID', ''),
        secret = os.environ.get('TWILIO_SECRET', ''),
        account = os.environ.get('TWILIO_ACCOUNT', ''),
        number = os.environ.get('TWILIO_NUMBER', '')
        )
else:
    app.config['twilio_account'] = users.TwilioAccount(
        sid = codecs.decode(os.environ.get('TWILIO_SID', ''), 'rot13'),
        secret = codecs.decode(os.environ.get('TWILIO_SECRET', ''), 'rot13'),
        account = codecs.decode(os.environ.get('TWILIO_ACCOUNT', ''), 'rot13'),
        number = os.environ.get('TWILIO_NUMBER', '')
        )

app.config['mailgun_account'] = users.MailgunAccount(
    api_key = os.environ.get('MAILGUN_API_KEY', ''),
    domain = os.environ.get('MAILGUN_DOMAIN', ''),
    sender = os.environ.get('MAILGUN_SENDER', 'alerts@verylittlegravitas.com')
    )

app.config['admin_credentials'] = dict(
    username = os.environ.get('ADMIN_USERNAME', 'admin'),
    password = os.environ.get('ADMIN_PASSWORD', 'admin'),
    )

@app.route('/')
def get_index():
    return flask.render_template('index.html', **template_kwargs())

@app.route('/about')
def get_about():
    return flask.render_template('about.html', **template_kwargs())

@app.route('/logout', methods=['POST'])
def post_logout():
    if 'phone_number' in flask.session:
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
            phone_number, zip_codes, email_address \
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
            phone_number, zip_codes, email_address \
                = users.get_user_info(db, flask.session['phone_number'])
        
    zip_code_str = ', '.join(zip_codes) if zip_codes else ''
    email_addr_str = email_address or ''
    return flask.render_template('profile.html', phone_number=phone_number,
                                 zip_codes=zip_code_str, email_address=email_addr_str,
                                 **template_kwargs())

@app.route('/profile', methods=['POST'])
@user_is_logged_in
def post_profile():
    print('FORM', flask.request.form)
    return 'UNDER CONSTRUCTION'

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
    print('POOP', email_address, 'from', address_encoded)
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
            emergencies.extend(wildfires.get_current_fires(db))
    return flask.render_template('admin.html', emergencies=emergencies,
                                 **template_kwargs())

@app.route('/admin/send-alert/<type>/<id>')
@user_is_an_admin
def get_send_alert(type, id):
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            if type == 'fire':
                emergency = wildfires.get_one_fire(db, id)
    return flask.render_template('send-alert.html', emergency=emergency,
                                 **template_kwargs())

@app.route('/admin/send-alert', methods=['POST'])
@user_is_an_admin
def post_send_alert():
    type = flask.request.form['emergency-type']
    id = flask.request.form['emergency-id']
    message = flask.request.form['emergency-message']
    twilio_account = flask.current_app.config['twilio_account']
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
            if type == 'fire':
                emergency = wildfires.get_one_fire(db, id)
                for user in notify.get_users_to_notify(db, emergency):
                    print('notify.send_notification:', user['phone_number'], emergency)
                    notify.send_notification(twilio_account, user['phone_number'], emergency)
    return flask.redirect(flask.url_for('get_sent_alert'), code=303)

@app.route('/admin/sent')
@user_is_an_admin
def get_sent_alert():
    return flask.render_template('sent.html', **template_kwargs())

@app.route('/stats')
def get_stats():
    return flask.render_template('stats.html', **template_kwargs())
