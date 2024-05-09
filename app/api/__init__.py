from flask import Blueprint
from flask_restful import Api

from .resources.admin_login import AdminLogin
from .resources.email_login import EmailLogin
from .resources.user_register import UserRegister
from .resources.user_login import UserLogin
from .resources.user_logout import UserLogout
from .resources.user_service import UserService
from .resources.admin_service import AdminService
from .resources.borrow_service import BorrowService
from .resources.captcha import Captcha

api_blueprint = Blueprint('api', __name__, url_prefix="/")
api = Api(api_blueprint)

api.add_resource(UserRegister, '/userRegister')
api.add_resource(UserLogin, '/userLogin', '/userRefreshToken')
api.add_resource(EmailLogin, '/emailLogin', '/userRefreshToken')
api.add_resource(AdminLogin, '/adminLogin', '/adminRefreshToken')
api.add_resource(UserLogout, '/userLogout')
api.add_resource(UserService, '/userInfo')
api.add_resource(AdminService, '/adminInfo')
api.add_resource(BorrowService, '/borrowInfo')
api.add_resource(Captcha, '/captcha')
