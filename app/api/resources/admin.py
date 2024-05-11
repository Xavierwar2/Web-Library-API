from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.admin_login import AdminLoginModel
from ..utils.format import res


class Admin(Resource):
    @jwt_required()
    def get(self):
        admin_login_list = AdminLoginModel.find_all()
        result = []
        for admin_login in admin_login_list:
            result.append(admin_login.dict())

        return res(data=result)

