from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user_info import UserModel
from ..utils.format import res


class User(Resource):
    @jwt_required()
    def get(self):
        user_info_list = UserModel.find_all()
        result = []
        for user_info in user_info_list:
            result.append(user_info.dict())

        return res(data=result)
