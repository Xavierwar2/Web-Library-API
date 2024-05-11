from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ..models.user_info import UserModel
from ..utils.format import res


class User(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            user_info_list = UserModel.find_all()
            result = []
            for user_info in user_info_list:
                result.append(user_info.dict())

            return res(data=result)

        else:
            return res(success=False, message='Access denied.', code=403)