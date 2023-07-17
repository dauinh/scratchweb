from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin
from flask_login import login_user

import utils

CONF_URL = 'https://pressingly-account.onrender.com'


def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = app.config['APP_SECRET']

    # Initialize Flask extensions
    db = SQLAlchemy()
    oauth = OAuth()

    # Setup Flask-SQLAlchemy
    db.init_app(app)
    oauth.init_app(app)
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

    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        email_confirmed_at = db.Column(db.DateTime())

        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')


    with app.app_context():
        db.create_all()

        # from models.user_model import User
        user_manager = UserManager(app, db, User)


        @app.context_processor
        def context_processor():
            return dict(user_manager=user_manager)


        @app.route('/')
        def home():
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
                username, email = utils.get_user_info(token)
                user = User.query.filter_by(username=username).first()
                if not user:
                    user = User(username=username)
                    db.session.add(user)
                    db.session.commit()
                login_user(user)
                return redirect('/profile')


        @app.route('/logout')
        def logout():
            session['token'] = None
            return redirect('/')


        @app.route('/profile')
        @login_required
        def profile():
            token = session['token']
            if not token:
                return redirect('/login')
            username, _ = utils.get_user_info(token)
            return render_template('profile.html', data=username)
    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True, ssl_context="adhoc")