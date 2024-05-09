import uuid

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from ..utils.format import res
from ..models.user_login import UserLoginModel
from ..models.user_info import UserModel
from ..schema.register_sha import reg_args_valid
from ..utils import redis_captcha


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        if UserLoginModel.find_by_username(username):
            return res(success=False, message="Repeated username!", code=400)
        elif UserModel.find_by_email(email):
            return res(success=False, message="Repeated email!", code=400)
        else:
            captcha = redis_captcha.redis_get(email)
            if captcha is None or captcha != data['captcha']:
                return res(success=False, message='Invalid captcha!', code=400)
            else:
                redis_captcha.redis_delete(email)
                try:
                    salt = uuid.uuid4().hex
                    password = generate_password_hash('{}{}'.format(salt, data['password']))
                    status = data['status']
                    user_login = UserLoginModel(username=username, password=password, salt=salt)
                    user_info = UserModel(username=username, email=email, status=status)
                    user_login.add()
                    user_info.add()
                    return res(message="Registration is successful!")
                except Exception as e:
                    return res(success=False, message="Error: {}".format(e), code=500)
