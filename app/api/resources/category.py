from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.book_info import BookModel
from datetime import datetime
from ..models.book_category import CategoryModel
from ..utils.format import res


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category_id', type=int, required=True, help='Category ID is required')
    parser.add_argument('category_name', type=str, required=True, help='Category name is required')

    @jwt_required()
    def get(self,category_id):
        category = CategoryModel.find_by_category_id(category_id)
        if category:
            book_category_list = CategoryModel.find_all()
            result = []
            for book_category in book_category_list:
                result.append(book_category.dict())
            return res(data=result)
        return res(message="Category not found", status=404)

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        category_name = data['category_name']
        new_category = CategoryModel(category_name=category_name)
        try:
            CategoryModel.add_book_category(new_category)
            return res(data=new_category.dict(), message="Category added successfully", status=201)
        except Exception as e:
            return res(message=str(e), status=500)

    @jwt_required()
    def delete(self, category_id):
        category_info = CategoryModel.find_by_category_id(category_id)
        if category_info:
            try:
                CategoryModel.delete_category_info(category_id)
                return res(message="Category deleted successfully", status=200)
            except Exception as e:
                return res(message=str(e), status=500)
        else:
            return res(message="Category not found", status=404)

    @jwt_required()
    def put(self, category_id):
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
