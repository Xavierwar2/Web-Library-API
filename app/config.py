import os
from datetime import timedelta

# 数据库相关配置
# 需要根据自己数据库的账号密码修改相关值
TYPE = "mysql+pymysql"
USERNAME = "root"
PASSWORD = "123456"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "web-library"


class Config:
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(TYPE, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access']
    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = "28038329@qq.com"
    MAIL_PASSWORD = "dsurhonxpksvcbaj"
    MAIL_DEFAULT_SENDER = "28038329@qq.com"


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
