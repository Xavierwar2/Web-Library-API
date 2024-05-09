from flask_restful import Resource, reqparse
from ..models.book_info import BookModel
from ..common.utils import res
from ..schema.book_sha import reg_args_valid


class BookAdd(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()
        try:
            book_name = data['book_name']
            author = data['author']
            text = data['text']
            image_url = data['image_url']
            number = data['number']
            category_id = data['category_id']
            product_id = data['product_id']
            book_info = BookModel(book_name=book_name, author=author, text=text, image_url=image_url,
                                  current_number=number, number=number, category_id=category_id,
                                  product_id=product_id)
            book_info.add()
            return res(message="Add Book successful!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)
