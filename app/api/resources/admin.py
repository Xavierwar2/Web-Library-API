import uuid

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash

from ..models.admin_login import AdminLoginModel
from ..schema.admin_sha import admin_args_valid
from ..utils.format import res


class AdminList(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']
        is_super = jwt_data['is_super']

        # 超级管理员可以执行该操作
        if role == 'admin' and is_super == 'true':
            admin_login_list = AdminLoginModel.find_all()
            result = []
            for admin_login in admin_login_list:
                result.append(admin_login.dict())

            return res(data=result)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        role = jwt_data['role']
        is_super = jwt_data['is_super']

        # 超级管理员可以执行该操作
        if role == 'admin' and is_super == 'true':
            parser = reqparse.RequestParser()
            admin_args_valid(parser)
            data = parser.parse_args()
            try:
                username = data['username']
                if AdminLoginModel.find_by_username(username):
                    return res(success=False, message="Repeated username!", code=400)
                else:
                    salt = uuid.uuid4().hex
                    password = generate_password_hash('{}{}'.format(salt, data['password']))
                    is_super_admin = data['is_super_admin']
                    admin_login = AdminLoginModel(username=username, password=password, salt=salt,
                                                  is_super_admin=is_super_admin)
                    admin_login.add()
                    return res(message="Add Admin successfully!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class Admin(Resource):
    @jwt_required()
    def get(self, admin_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            admin_login = AdminLoginModel.find_by_admin_id(admin_id)
            if admin_login:
                return res(data=admin_login.dict())
            else:
                return res(message="Admin not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def delete(self, admin_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                AdminLoginModel.delete_by_admin_id(admin_id)
                return res(message='Admin deleted successfully!')
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def put(self, admin_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            admin_args_valid(parser)
            data = parser.parse_args()
            try:
                admin_login = AdminLoginModel.find_by_admin_id(admin_id)
                if admin_login:
                    username = data['username']
                    if username != admin_login.username and AdminLoginModel.find_by_username(username):
                        return res(success=False, message="Repeated username!", code=400)
                    else:
                        salt = admin_login.salt
                        password = admin_login.password
                        if data['password']:
                            salt = uuid.uuid4().hex
                            password = generate_password_hash('{}{}'.format(salt, data['password']))
                        is_super_admin = data['is_super_admin']
                        admin_login.update_admin(admin_id, username, password, salt, is_super_admin)
                        return res(message="Update Admin successfully!")
                else:
                    return res(success=False, message="Admin not found", code=404)
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)
