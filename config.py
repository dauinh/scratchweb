import os

# Class-based application configuration
# class ConfigClass(object):
#     """ Flask application config """

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///scratchweb.sqlite'    # File-based SQL database
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

# Flask-User settings
USER_APP_NAME = "Scratch App"     # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

OIDC_CLIENT_ID = os.getenv('OIDC_CLIENT_ID')
OIDC_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET')
APP_SECRET = os.getenv('APP_SECRET')