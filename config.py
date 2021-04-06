import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A very secret key!Hohoho!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    def __init__(self) -> None:
        if 'postgres://' in Config.SQLALCHEMY_DATABASE_URI:
            Config.SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.replace(
                "postgres://", "postgresql://", 1)
