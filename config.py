import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is very secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DISCORD_OAUTH_SECRET_KEY = 'FjMSodOATz4FoXByylp6QS0lWQLeYKWa'
    DISCORD_OAUTH_CLIENT_ID = '440052776702312450'
