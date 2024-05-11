from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash

from ..schema.register_sha import reg_args_valid
from ..models.admin_login import AdminLoginModel
from ..utils.format import res


class AdminLogin(Resource):
    def post(self):
        # 初始化解析器
        parser = reqparse.RequestParser()
        # 添加请求参数校验
        reg_args_valid(parser)
        data = parser.parse_args()
        username = data['username']
        admin_login = AdminLoginModel.find_by_username(username)
        if admin_login:
            try:
                password, salt = admin_login.password, admin_login.salt
                valid = check_password_hash(password, '{}{}'.format(salt, data['password']))
                if valid:
                    # 生成 token
                    response_data = generate_token(username)
                    return res(response_data)
                else:
                    raise ValueError('Invalid password!')
            except Exception as e:
                return res(success=False, message='Error: {}'.format(e), code=500)
        else:
            return res(success=False, message='Unregistered username!', code=400)

    @jwt_required(refresh=True)
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']
        is_super = jwt_data['is_super']

        # 管理员可以执行该操作
        if role == 'admin':
            # access_token 过期后 需要用 refresh_token 来换取新的 token
            # 先从 refresh_token 中取出用户信息
            current_username = get_jwt_identity()
            # 再生成新的 token
            if is_super == 'true':
                access_token = create_access_token(identity=current_username,
                                                   additional_claims={'role': 'admin', 'is_super': 'true'})
                return res(data={'accessToken': 'Bearer ' + access_token})
            elif is_super == 'false':
                access_token = create_access_token(identity=current_username,
                                                   additional_claims={'role': 'admin', 'is_super': 'false'})
                return res(data={'accessToken': 'Bearer ' + access_token})
            else:
                return res(success=False, message='Access denied.', code=403)

        else:
            return res(success=False, message='Access denied.', code=403)


# 生成token
def generate_token(id):
    admin_login = AdminLoginModel.find_by_username(id)

    if admin_login.is_super_admin:
        access_token = create_access_token(identity=id, additional_claims={'role': 'admin', 'is_super': 'true'})
        refresh_token = create_refresh_token(identity=id, additional_claims={'role': 'admin', 'is_super': 'true'})
    else:
        access_token = create_access_token(identity=id, additional_claims={'role': 'admin', 'is_super': 'false'})
        refresh_token = create_refresh_token(identity=id, additional_claims={'role': 'admin', 'is_super': 'false'})
    return {
        'accessToken': 'Bearer ' + access_token,
        'refreshToken': 'Bearer ' + refresh_token,
    }
