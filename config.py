"""
Configuration for Flask Application 'Virtual Watershed Platform'
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('VW_SECRET_KEY') or 'hard to guess string'
    MONGODB_SETTINGS = {'db': 'rda_lod'}

    DEVELOPMENT = False
    DEBUG = False
    PRODUCTION = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
