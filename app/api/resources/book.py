from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.book_info import BookModel
from ..schema.book_sha import book_args_valid
from ..utils.format import res


class BookListService(Resource):
    @jwt_required()
    def get(self):
        book_info_list = BookModel.find_all()
        result = []
        for book_info in book_info_list:
            result.append(book_info.dict())

        return res(data=result)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        book_args_valid(parser)
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


class BookService(Resource):
    @jwt_required()
    def get(self, book_id):
        book_info_list = BookModel.find_all()
        if book_id:
            book_info = BookModel.find_by_book_id(book_id)
            if book_info:
                for book_info in book_info_list:
                    if book_info.book_id == book_id:
                        return res(data=book_info.dict())
            else:
                return res(message="Book not found", code=404)
        else:
            result = [book_info.dict() for book_info in book_info_list]
            return res(data=result)

    @jwt_required()
    def delete(self, book_id):
        try:
            BookModel.delete_by_book_id(book_id)
            return res(message='Book deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        book_args_valid(parser)
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
