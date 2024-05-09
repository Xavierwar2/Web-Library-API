from flask_restful import Resource, reqparse

from ..models.book_info import BookModel
from app.api.common.utils import res
from app.api.schema.book_sha import reg_args_valid


class BookDelete(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()
        try:
            book_id = data['book_id']
            BookModel.delete_by_book_id(book_id)
            return res(message='Book deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

