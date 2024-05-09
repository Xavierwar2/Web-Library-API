from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.book_info import BookModel
from ..common.utils import res


class BookService(Resource):
    @jwt_required()
    def get(self):
        book_info_list = BookModel.find_all()
        result = []
        for book_info in book_info_list:
            result.append(book_info.dict())

        return res(data=result)
