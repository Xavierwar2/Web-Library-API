import os
import logging
from logging.handlers import RotatingFileHandler
import time
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

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
from .api.models.notice_info import NoticeModel


def create_app(config_name):
    # 初始化 Flask 项目
    app = Flask(__name__)
    # 加载配置项
    app.config.from_object(config[config_name])
    
    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/web-library.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Web Library startup')
    
    # 请求前后钩子，用于性能监控
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        # 添加安全相关的响应头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 记录请求处理时间
        if hasattr(request, 'start_time'):
            elapsed = time.time() - request.start_time
            app.logger.info(f'Request to {request.path} took {elapsed:.2f}s')
        return response

    # 全局错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'message': '请求的资源不存在'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return jsonify({'message': '服务器内部错误'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled Exception: {error}')
        return jsonify({'message': '服务器发生未知错误'}), 500

    # 支持代理服务器
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # 初始化各种扩展
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_blueprint)
    jwt = JWTManager(app)
    register_jwt_hooks(jwt)
    CORS(app)
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
