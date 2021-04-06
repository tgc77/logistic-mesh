import os

basedir = os.path.abspath(os.path.dirname(__file__))


def validate_database_url(database_url: str) -> str:
    if database_url is not None and 'postgres://' in database_url:
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    return database_url


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A very secret key!Hohoho!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = validate_database_url(os.environ.get('DATABASE_URL')) or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
