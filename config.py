import os
TESTING_DATABASE_URI = 'sqlite:///test.db'
DATABASE_URI = 'sqlite:///dsp_rtb.db'
API_URL = 'http://hsuehkuanlu.ddns.net'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SECRET_KEY = 'secret-key'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
