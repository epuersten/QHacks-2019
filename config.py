import os, pymysql
basedir = os.path.abspath(os.path.dirname(__file__))

######################
# CONFIGURATIONS
######################
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qhacks2019'

    # FLASK-MAIL
    # https://pythonhosted.org/Flask-Mail/
    MAIL_SERVER         = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT           = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS        = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME       = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD       = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or ''
    # LOGGER
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') # Investigate logger

    # SQL ALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER =  os.path.join(basedir, 'upload_folder')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

######################
# ENVIRONMENTS
######################
class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root@localhost:3306/qhacksdb'

app_config = {
    'development': DevelopmentConfig,
    }
