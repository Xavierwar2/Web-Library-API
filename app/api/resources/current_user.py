from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource

from ..models.admin_login import AdminLoginModel
from ..models.user_info import UserModel
from ..utils.format import res


class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        current_username = get_jwt_identity()
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 普通用户得到自身信息
        if role == 'user':
            user_info = UserModel.find_by_username(current_username)
            if user_info:
                print()
                return res(data=user_info.dict())
            else:
                return res(success=False, message="User not found", code=404)

        # 管理员得到自身信息
        if role == 'admin':
            admin_login = AdminLoginModel.find_by_username(current_username)
            if admin_login:
                return res(data=admin_login.dict())
            else:
                return res(success=False, message="Admin not found", code=404)

        return res(success=False, message='Access denied.', code=403)
