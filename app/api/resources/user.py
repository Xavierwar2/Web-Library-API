from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.user_info import UserModel
from ..schema.user_sha import user_args_valid
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
        try:
            UserModel.delete_by_user_id(user_id)
            UserLoginModel.delete_by_user_id(user_id)
            return res(message='User deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def put(self, user_id):
        parser = reqparse.RequestParser()
        user_args_valid(parser)
        data = parser.parse_args()
        try:
            user_info = UserModel.find_by_user_id(user_id)
            if user_info:
                username = data['username']
                email = data['email']
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
        user_info_list = UserModel.find_all()
        result = []
        for user_info in user_info_list:
            result.append(user_info.dict())

        return res(data=result)


class UserByUsername(Resource):
    @jwt_required()
    def get(self, username):
        user_info = UserModel.find_by_username(username)
        print(username)
        if user_info:
            return user_info.dict()
        else:
            return res(message="User not found", code=404)
