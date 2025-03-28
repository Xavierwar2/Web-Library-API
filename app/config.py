import os
from datetime import timedelta

# 数据库相关配置
TYPE = os.getenv('DB_TYPE', 'mysql+pymysql')
USERNAME = os.getenv('DB_USERNAME', 'root')
PASSWORD = os.getenv('DB_PASSWORD', '')
HOST = os.getenv('DB_HOST', '127.0.0.1')
PORT = os.getenv('DB_PORT', '3306')
DATABASE = os.getenv('DB_NAME', 'web-library')


class Config:
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(TYPE, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 缓存配置
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_HOURS', '2')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_DAYS', '30')))
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access']
    # 邮箱配置
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.qq.com')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
