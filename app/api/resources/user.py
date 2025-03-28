import uuid
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash

from ..models.user_info import UserModel
from ..schema.user_sha import user_args_valid
from ..utils import redis_captcha
from ..utils.format import res
from ..models.user_login import UserLoginModel
from .base import BaseResource
from ..extensions import cache


class User(BaseResource):
    @jwt_required()
    @cache.memoize(300)
    def get(self, user_id):
        """获取用户信息"""
        try:
            user_info = self.validate_exists(UserModel, user_id, 'user_id')
            if user_info:
                return user_info.dict()
            return res(message="User not found", code=404)
        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def delete(self, user_id):
        """删除用户"""
        @self.admin_required
        def delete_user():
            try:
                UserModel.delete_by_user_id(user_id)
                UserLoginModel.delete_by_user_id(user_id)
                # 清除缓存
                cache.delete_memoized(self.get, user_id)
                cache.delete('user_list')
                return res(message='User deleted successfully!')
            except Exception as e:
                return self.handle_error(e)
        return delete_user()

    @jwt_required()
    def put(self, user_id):
        """更新用户信息"""
        try:
            data = self._parse_user_args()
            user_info = self.validate_exists(UserModel, user_id, 'user_id')
            user_login = self.validate_exists(UserLoginModel, user_id, 'user_id')
            
            if not user_info or not user_login:
                return res(success=False, message="User not found", code=404)
            
            # 检查用户名是否重复
            if self._is_username_duplicate(data['username'], user_login.username):
                return res(success=False, message="Repeated username!", code=400)
            
            # 处理密码更新
            if data['password']:
                self._update_password(user_id, data['password'], user_login)
                return res(message="Update password successfully!")
            
            # 处理邮箱验证
            if data['email'] and not self._verify_captcha(data['email'], data['captcha']):
                return res(success=False, message='Invalid captcha!', code=400)
            
            # 更新用户信息
            self._update_user_info(user_info, user_id, data)
            
            # 清除缓存
            cache.delete_memoized(self.get, user_id)
            cache.delete('user_list')
            
            return res(message="Update User successfully!")
        except Exception as e:
            return self.handle_error(e)

    def _parse_user_args(self):
        """解析用户参数"""
        parser = reqparse.RequestParser()
        user_args_valid(parser)
        return parser.parse_args()

    def _is_username_duplicate(self, new_username, old_username):
        """检查用户名是否重复"""
        return new_username != old_username and UserLoginModel.find_by_username(new_username)

    def _update_password(self, user_id, password, user_login):
        """更新用户密码"""
        salt = uuid.uuid4().hex
        hashed_password = generate_password_hash(f'{salt}{password}')
        user_login.update_user(user_id, user_login.username, hashed_password, salt)

    def _verify_captcha(self, email, captcha):
        """验证邮箱验证码"""
        stored_captcha = redis_captcha.redis_get(email)
        if stored_captcha and stored_captcha == captcha:
            redis_captcha.redis_delete(email)
            return True
        return False

    def _update_user_info(self, user_info, user_id, data):
        """更新用户基本信息"""
        user_info.update_user(
            user_id=user_id,
            username=data['username'],
            email=data['email'] or user_info.email,
            sex=data['sex'],
            age=data['age'],
            status=data['status'],
            image_url=data['image_url']
        )


class UserList(BaseResource):
    @jwt_required()
    @cache.cached(timeout=300, key_prefix='user_list')
    def get(self):
        """获取所有用户列表"""
        @self.admin_required
        def get_all_users():
            try:
                user_info_list = UserModel.find_all()
                return res(data=[user_info.dict() for user_info in user_info_list])
            except Exception as e:
                return self.handle_error(e)
        return get_all_users()

    @jwt_required()
    def delete(self):
        """批量删除用户"""
        @self.admin_required
        def delete_users():
            try:
                data = self._parse_user_args()
                delete_list = data['delete_list']
                
                for user in delete_list:
                    user_id = user.get('user_id')
                    if user_id:
                        UserModel.delete_by_user_id(user_id)
                        UserLoginModel.delete_by_user_id(user_id)
                        # 清除单个用户缓存
                        cache.delete_memoized(User.get, User, user_id)
                
                # 清除用户列表缓存
                cache.delete('user_list')
                return res(message='Users deleted successfully!')
            except Exception as e:
                return self.handle_error(e)
        return delete_users()

    def _parse_user_args(self):
        """解析用户参数"""
        parser = reqparse.RequestParser()
        user_args_valid(parser)
        return parser.parse_args()


class UserByUsername(BaseResource):
    @jwt_required()
    @cache.memoize(300)
    def get(self, username):
        """通过用户名获取用户信息"""
        @self.admin_required
        def get_user_by_username():
            try:
                user_info = UserModel.find_by_username(username)
                if user_info:
                    return user_info.dict()
                return res(message="User not found", code=404)
            except Exception as e:
                return self.handle_error(e)
        return get_user_by_username()