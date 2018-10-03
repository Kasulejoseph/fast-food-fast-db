import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:password@localhost/food_db'


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:password@localhost/test_db'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
