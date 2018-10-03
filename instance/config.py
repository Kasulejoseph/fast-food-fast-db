import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = 'postgres://mlmjbgdiusgkek:42f5c949ece6dd260303c77682bffb55cb2a53cd8973435a1e8bb3fd0de1abe2@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dbigg45nbqe6jq'

class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/test_db'

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
