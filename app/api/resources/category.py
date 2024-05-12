from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from ..models.book_info import BookModel
from ..models.book_category import CategoryModel
from ..utils.format import res


class CategoryList(Resource):
    def get(self):
        book_category_list = CategoryModel.find_all()
        result = []
        for book_category in book_category_list:
            result.append(book_category.dict())

        return res(data=result)

    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('category_id', type=int, required=True, help='Category ID is required')
            parser.add_argument('category_name', type=str, required=True, help='Category name is required')

            data = self.parser.parse_args()
            category_name = data['category_name']
            new_category = CategoryModel(category_name=category_name)
            try:
                CategoryModel.add_book_category(new_category)
                return res(data=new_category.dict(), message="Category added successfully", status=201)
            except Exception as e:
                return res(message=str(e), status=500)
            
        else:
            return res(success=False, message='Access denied.', code=403)


class Category(Resource):
    def get(self, category_id):
        book_category = BookModel.find_by_category_id(category_id)
        if book_category:
            return res(data=book_category.dict())
        else:
            return res(message="Book not found", code=404)

    @jwt_required()
    def delete(self, category_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            category_info = CategoryModel.find_by_category_id(category_id)
            if category_info:
                try:
                    CategoryModel.delete_category_info(category_id)
                    book_category = BookModel.find_by_category_id(category_id)
                    for book in book_category:
                        book_id = book.get('book_id')
                        book.update_book_category_id(book_id, 0)
                    return res(message="Category deleted successfully", status=200)
                except Exception as e:
                    return res(message=str(e), status=500)
            else:
                return res(message="Category not found", status=404)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def put(self, category_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
        
            data = self.parser.parse_args()
            category_name = data['category_name']
            category_info = CategoryModel.find_by_category_id(category_id)
            if category_info:
                try:
                    CategoryModel.update(category_id, category_name)
                    return res(message="Category updated successfully", status=200)
                except Exception as e:
                    return res(message=str(e), status=500)
            else:
                return res(message="Category not found", status=404)
        
        else:
            return res(success=False, message='Access denied.', code=403)
