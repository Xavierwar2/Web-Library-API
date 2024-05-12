from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from ..models.book_info import BookModel
from ..schema.book_sha import book_args_valid
from ..utils.format import res


class BookList(Resource):
    def get(self):
        book_info_list = BookModel.find_all()
        result = []
        for book_info in book_info_list:
            result.append(book_info.dict())

        return res(data=result)

    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
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
                return res(message="Add Book successfully!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def delete(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                parser = reqparse.RequestParser()
                book_args_valid(parser)
                data = parser.parse_args()
                delete_list = data['delete_list']
                # 根据提供的 ID 数组执行删除操作
                for user in delete_list:
                    book_id = user.get('book_id')
                    BookModel.delete_by_book_id(book_id)
                return res(message='Books deleted successfully!')

            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class Book(Resource):
    def get(self, book_id):
        book_info = BookModel.find_by_book_id(book_id)
        if book_info:
            return res(data=book_info.dict())
        else:
            return res(message="Book not found", code=404)

    @jwt_required()
    def delete(self, book_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                BookModel.delete_by_book_id(book_id)
                return res(message='Book deleted successfully!')
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def put(self, book_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            book_args_valid(parser)
            data = parser.parse_args()
            try:
                book_info = BookModel.find_by_book_id(book_id)
                if book_info:
                    book_info.book_name = data['book_name']
                    book_info.author = data['author']
                    book_info.text = data['text']
                    book_info.image_url = data['image_url']
                    book_info.current_number = data['current_number']
                    book_info.number = data['number']
                    book_info.category_id = data['category_id']
                    book_info.product_id = data['product_id']
                    BookModel.update_book_info(book_info)
                    return res(message="Update Book successfully!")
                else:
                    return res(success=False, message="Book not found", code=404)
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)
