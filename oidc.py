import requests

from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth


CONF_URL = 'https://pressingly-account.onrender.com'

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['APP_SECRET']

oauth = OAuth(app)
oauth.register(
    name='pressingly',
    client_id=app.config['OIDC_CLIENT_ID'],
    client_secret=app.config['OIDC_CLIENT_SECRET'],
    access_token_url=f'{CONF_URL}/oauth/token',
    access_token_params=None,
    authorize_url=f'{CONF_URL}/oauth/authorize',
    authorize_params=None,
    # api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'openid email'},
    server_metadata_url=f'{CONF_URL}/.well-known/openid-configuration'
)


pressingly = oauth.pressingly

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    pressingly = oauth.create_client('pressingly')
    redirect_uri = url_for('auth', _external=True)
    return pressingly.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.pressingly.authorize_access_token()
    if token:
        session['token'] = token
    return redirect('/profile')


@app.route('/profile')
def profile():
    token = session['token']
    access_token = token['access_token']
    userInfoEndpoint = f'{CONF_URL}/oauth/userinfo'
    userInfoResponse = requests.post(userInfoEndpoint,
                                    headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'})
    return render_template('profile.html', data=userInfoResponse.json())

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, ssl_context="adhoc")
