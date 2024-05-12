import uuid

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash

from ..models.user_info import UserModel
from ..schema.user_sha import user_args_valid
from ..utils import redis_captcha
from ..utils.format import res
from ..models.user_login import UserLoginModel


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        user_info = UserModel.find_by_user_id(user_id)
        if user_info:
            return user_info.dict()
        else:
            return res(message="User not found", code=404)

    @jwt_required()
    def delete(self, user_id):
        jwt_data = get_jwt()
        role = jwt_data['role']
        if role == 'admin':
            try:
                UserModel.delete_by_user_id(user_id)
                UserLoginModel.delete_by_user_id(user_id)
                return res(message='User deleted successfully!')
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)
        else:
            return res(success=False, message="Role must be admin")

    @jwt_required()
    def put(self, user_id):
        parser = reqparse.RequestParser()
        user_args_valid(parser)
        data = parser.parse_args()
        try:
            user_info = UserModel.find_by_user_id(user_id)
            user_login = UserLoginModel.find_by_user_id(user_id)
            if user_info and user_login:
                username = data['username']
                if username != user_login.username and UserLoginModel.find_by_username(username):
                    return res(success=False, message="Repeated username!", code=400)
                else:
                    if data['password']:
                        salt = uuid.uuid4().hex
                        password = generate_password_hash('{}{}'.format(salt, data['password']))
                        user_login.update_user(user_id, username, password, salt)
                        return res(message="Update password successfully!")

                    email = user_info.email
                    if data['email']:
                        email = data['email']
                        captcha = redis_captcha.redis_get(email)
                        if captcha is None or captcha != data['captcha']:
                            return res(success=False, message='Invalid captcha!', code=400)
                        else:
                            redis_captcha.redis_delete(email)

                    sex = data['sex']
                    age = data['age']
                    status = data['status']
                    image_url = data['image_url']
                    user_info.update_user(user_id, username, email, sex, age, status, image_url)
                    return res(message="Update User successfully!")
            else:
                return res(success=False, message="User not found", code=404)
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)


class UserList(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']
        if role == 'admin':
            user_info_list = UserModel.find_all()
            result = []
            for user_info in user_info_list:
                result.append(user_info.dict())
            return res(data=result)
        else:
            return res(success=False, message="Role must be admin", code=403)

    @jwt_required()
    def delete(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                parser = reqparse.RequestParser()
                user_args_valid(parser)
                data = parser.parse_args()
                delete_list = data['delete_list']
                # 根据提供的 ID 数组执行删除操作
                for user in delete_list:
                    user_id = user.get('user_id')
                    UserModel.delete_by_user_id(user_id)
                    UserLoginModel.delete_by_user_id(user_id)
                return res(message='Users deleted successfully!')

            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class UserByUsername(Resource):
    @jwt_required()
    def get(self, username):
        jwt_data = get_jwt()
        role = jwt_data['role']
        if role == 'admin':
            user_info = UserModel.find_by_username(username)
            if user_info:
                return user_info.dict()
            else:
                return res(message="User not found", code=404)
        else:
            return res(success=False, message='Access denied.', code=403)