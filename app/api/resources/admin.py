from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ..models.admin_login import AdminLoginModel
from ..utils.format import res


class Admin(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            admin_login_list = AdminLoginModel.find_all()
            result = []
            for admin_login in admin_login_list:
                result.append(admin_login.dict())

            return res(data=result)

        else:
            return res(success=False, message='Access denied.', code=403)
