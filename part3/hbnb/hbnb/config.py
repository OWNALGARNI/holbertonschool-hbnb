import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_change_in_production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLite for development
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///hbnb_dev.db'
    )

class ProductionConfig(Config):
    DEBUG = False
    # MySQL for production
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:password@localhost/hbnb_prod'
    )

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
