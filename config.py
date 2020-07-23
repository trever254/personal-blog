import os

class Config:
    QUOTE_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # simple mde configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/blogs'
    pass

config_options = {
    'development':DevConfig,
    'production':ProdConfig
}
