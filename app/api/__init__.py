from flask import Blueprint
from flask_restful import Api

from .resources.admin_login import AdminLogin
from .resources.user_register import UserRegister
from .resources.user_login import UserLogin
from .resources.user_logout import UserLogout
from .resources.user_service import UserService

api_blueprint = Blueprint('api', __name__, url_prefix="/")
api = Api(api_blueprint)

api.add_resource(UserRegister, '/userRegister')
api.add_resource(UserLogin, '/userLogin', '/userRefreshToken')
api.add_resource(AdminLogin, '/adminLogin', '/adminRefreshToken')
api.add_resource(UserLogout, '/userLogout')
api.add_resource(UserService, '/userInfo')
