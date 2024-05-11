import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config
from .api.models import db
from .extensions import mail
from .api import api_blueprint
from .manage import migrate
from .api.models.user_info import UserModel
from .api.models.revoked_token import RevokedTokenModel
from .api.models.user_login import UserLoginModel
from .api.models.admin_login import AdminLoginModel
from .api.models.user_collect import CollectModel
from .api.models.user_feedback import FeedbackModel
from .api.models.user_comment import CommentModel
from .api.models.book_info import BookModel
from .api.models.book_category import CategoryModel
from .api.models.book_product import ProductModel
from .api.models.borrow_info import BorrowModel


def create_app(config_name):
    # 初始化 Flask 项目
    app = Flask(__name__)
    # 加载配置项
    app.config.from_object(config[config_name])
    # 初始化数据库ORM
    db.init_app(app)
    # 初始化数据库ORM迁移插件
    migrate.init_app(app, db)
    # 注册蓝图
    app.register_blueprint(api_blueprint)
    # 初始化 JWT
    jwt = JWTManager(app)
    # 注册 JWT 钩子
    register_jwt_hooks(jwt)
    # 解决跨域
    CORS(app)
    # 添加邮箱验证机制
    mail.init_app(app)
    return app


def register_jwt_hooks(jwt):
    # 注册 JWT 钩子 用于检查 token 是否在黑名单中
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


# 初始化项目
app = create_app(os.getenv('FLASK_ENV', 'development'))
