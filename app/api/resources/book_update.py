from flask_restful import reqparse, Resource
from ..models.book_info import BookModel
from ..common.utils import res
from ..schema.book_sha import reg_args_valid


class BookUpdate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()
        try:
            book_info = BookModel.find_by_book_id(data['book_id'])
            if book_info:
                book_name = data['book_name']
                author = data['author']
                text = data['text']
                image_url = data['image_url']
                current_number = data['current_number']
                number = data['number']
                category_id = data['category_id']
                product_id = data['product_id']
                book_info = BookModel(book_id=data['book_id'], book_name=book_name, author=author, text=text,
                                      image_url=image_url, current_number=current_number, number=number,
                                      category_id=category_id, product_id=product_id)
                book_info.update_book(data['book_id'], book_name, author, text, image_url, current_number, number,
                                      category_id, product_id)
                return res(message="Update Book successful!")
            else:
                return res(success=False, message="Book not found", code=404)
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)
