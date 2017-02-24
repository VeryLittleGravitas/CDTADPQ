import flask, codecs, psycopg2, os, json, functools, sys
from ..data import users, zipcodes

def user_is_logged_in(untouched_route):
    '''
    '''
    @functools.wraps(untouched_route)
    def wrapper(*args, **kwargs):
        if 'phone_number' not in flask.session:
            body = flask.render_template('error-auth.html', **template_kwargs())
            return flask.Response(body, status=401)

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
            signup_id = users.add_unverified_signup(db, twilio_account, to_number)
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
    return flask.render_template('confirmation.html', **template_kwargs())

@app.route('/profile')
@user_is_logged_in
def get_profile():
    return flask.render_template('profile.html', **template_kwargs())

@app.route('/admin')
def get_admin():
    return flask.render_template('admin.html', **template_kwargs())

@app.route('/send-alert')
def get_sendalert():
    return flask.render_template('send-alert.html', **template_kwargs())

@app.route('/sent')
def get_sent():
    return flask.render_template('sent.html', **template_kwargs())

@app.route('/stats')
def get_stats():
    return flask.render_template('stats.html', **template_kwargs())
