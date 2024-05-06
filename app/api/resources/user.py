from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user_info import UserModel
from ..common.utils import res


class UserService(Resource):
    @jwt_required()
    def get(self):
        user_list = UserModel.get_all_user()
        result = []
        for user in user_list:
            result.append(user.dict())

        return res(data=result)

