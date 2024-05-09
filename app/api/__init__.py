from flask import Blueprint
from flask_restful import Api

from .resources.admin_login import AdminLogin
from .resources.user_register import UserRegister
from .resources.user_login import UserLogin
from .resources.user_logout import UserLogout
from .resources.user_service import UserService
from .resources.book_service import BookService
from .resources.book_add import BookAdd
from .resources.book_delete import BookDelete
from .resources.book_update import BookUpdate


api_blueprint = Blueprint('api', __name__, url_prefix="/")
api = Api(api_blueprint)

api.add_resource(UserRegister, '/userRegister')
api.add_resource(UserLogin, '/userLogin', '/userRefreshToken')
api.add_resource(AdminLogin, '/adminLogin', '/adminRefreshToken')
api.add_resource(UserLogout, '/userLogout')
api.add_resource(UserService, '/userInfo')
api.add_resource(BookService, '/bookInfo')
api.add_resource(BookAdd, '/bookAdd')
api.add_resource(BookDelete, '/bookDelete')
api.add_resource(BookUpdate, '/bookUpdate')
