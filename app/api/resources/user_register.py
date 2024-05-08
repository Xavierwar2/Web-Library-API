import uuid

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from ..common.utils import res
from ..models.user_login import UserLoginModel
from ..models.user_info import UserModel
from ..schema.register_sha import reg_args_valid


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()
        if UserLoginModel.find_by_username(data['username']):
            return res(success=False, message="Repeated username!", code=400)
        else:
            try:
                username = data['username']
                salt = uuid.uuid4().hex
                password = generate_password_hash('{}{}'.format(salt, data['password']))
                email = data['email']
                status = data['status']
                user_login = UserLoginModel(username=username, password=password, salt=salt)
                user_info = UserModel(username=username, email=email, status=status)
                user_login.add()
                user_info.add()
                return res(message="Registration is successful!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)
