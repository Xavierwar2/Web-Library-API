from flask import Blueprint
from flask_restful import Api

from .resources.admin_login import AdminLogin
from .resources.comment import Comment, CommentList, CommentByUser, CommentByBook
from .resources.email_login import EmailLogin
from .resources.user_register import UserRegister
from .resources.user_login import UserLogin
from .resources.user_logout import UserLogout
from .resources.user import UserList
from .resources.user import User
from .resources.user import UserByUsername
from .resources.book import BookList
from .resources.book import Book
from .resources.product import Product
from .resources.category import Category

from .resources.admin import Admin
from .resources.borrow import Borrow
from .resources.captcha import Captcha

api_blueprint = Blueprint('api', __name__, url_prefix="/")
api = Api(api_blueprint)

api.add_resource(UserRegister, '/userRegister')
api.add_resource(UserLogin, '/userLogin', '/userRefreshToken')
api.add_resource(EmailLogin, '/emailLogin', '/userRefreshToken')
api.add_resource(AdminLogin, '/adminLogin', '/adminRefreshToken')
api.add_resource(UserLogout, '/userLogout')
api.add_resource(User, '/userInfo/<int:user_id>')
api.add_resource(UserList, '/userListInfo')
api.add_resource(UserByUsername, '/userInfo/<string:username>')
api.add_resource(Admin, '/adminInfo')
api.add_resource(Borrow, '/borrowInfo')
api.add_resource(Captcha, '/captcha')
api.add_resource(BookList, '/bookInfo')
api.add_resource(Book, '/bookInfo/<int:book_id>')
api.add_resource(Product, '/productInfo')
api.add_resource(Category, '/categoryInfo')
api.add_resource(CommentList, '/comment')
api.add_resource(Comment, '/comment/<int:comment_id>')
api.add_resource(CommentByUser, '/comment/user/<int:user_id>')
api.add_resource(CommentByBook, '/comment/book/<int:book_id>')
