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
            parser.add_argument('category_name', type=str, required=True, help='Category name is required')
            data = parser.parse_args()
            category_name = data['category_name']
            if CategoryModel.find_by_category_name(category_name):
                return res(success=False, message="Repeated username!", code=400)

            new_category = CategoryModel(category_name=category_name)
            try:
                new_category.add()
                return res(message="Category added successfully", code=200)
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class Category(Resource):
    def get(self, category_id):
        book_category = CategoryModel.find_by_category_id(category_id)
        if book_category:
            return res(data=book_category.dict())
        else:
            return res(message="Category not found", code=404)

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
                    book_info_list = BookModel.find_by_category_id(category_id)
                    for book_info in book_info_list:
                        book_info.category_id = 0
                        BookModel.update_book_info(book_info)
                    return res(message="Category deleted successfully", code=200)
                except Exception as e:
                    return res(success=False, message="Error: {}".format(e), code=500)
            else:
                return res(success=False, message="Category not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def put(self, category_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('category_name', type=str, required=True, help='Category name is required')
            data = parser.parse_args()
            category_name = data['category_name']
            category_info = CategoryModel.find_by_category_id(category_id)
            if category_info:
                try:
                    CategoryModel.update(category_id, category_name)
                    return res(message="Category updated successfully", code=200)
                except Exception as e:
                    return res(success=False, message="Error: {}".format(e), code=500)
            else:
                return res(success=False, message="Category not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)
