from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from ..schema.email_verify_sha import email_verify_args_valid
from ..models.user_login import UserLoginModel
from ..utils import redis_captcha
from ..utils.format import res
from ..models.user_info import UserModel


class EmailLogin(Resource):
    def post(self):
        # 初始化解析器
        parser = reqparse.RequestParser()
        # 添加请求参数校验
        email_verify_args_valid(parser)
        data = parser.parse_args()
        email = data['email']
        info_tuple = UserModel.find_by_email(email)
        if info_tuple:
            captcha = redis_captcha.redis_get(email)
            if captcha is None or captcha != data['captcha']:
                return res(success=False, message='Invalid captcha!', code=400)
            else:
                redis_captcha.redis_delete(email)
                try:
                    (info,) = info_tuple
                    username = info.username
                    login_tuple = UserLoginModel.find_by_username(username)
                    if login_tuple:
                        # 生成 token
                        response_data = generate_token(username)
                        return res(response_data)
                    else:
                        return res(success=False, message='Unregistered username!', code=400)
                except Exception as e:
                    return res(success=False, message='Error: {}'.format(e), code=500)
        else:
            return res(success=False, message='Unregistered email!', code=400)

    @jwt_required(refresh=True)
    def get(self):
        # access_token 过期后 需要用 refresh_token 来换取新的 token
        # 先从 refresh_token 中取出用户信息
        current_username = get_jwt_identity()
        # 再生成新的 token
        access_token = create_access_token(identity=current_username, additional_claims={'role': 'user'})
        return res(data={'accessToken': 'Bearer ' + access_token})


# 生成token
def generate_token(id):
    access_token = create_access_token(identity=id, additional_claims={'role': 'user'})
    refresh_token = create_refresh_token(identity=id, additional_claims={'role': 'user'})
    return {
        'accessToken': 'Bearer ' + access_token,
        'refreshToken': 'Bearer ' + refresh_token,
    }
