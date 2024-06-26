from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from ..models.book_info import BookModel
from datetime import datetime
from ..models.book_product import ProductModel
from ..utils.format import res


class ProductList(Resource):

    @jwt_required()
    def get(self):
        book_product_list = ProductModel.find_all()
        result = []
        for book_product in book_product_list:
            result.append(book_product.dict())

        return res(data=result)
    
    @jwt_required()
    def post(self):

        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
            parser.add_argument('product_name', type=str, required=True, help='Product name is required')
            parser.add_argument('category_id', type=int, required=True, help='Category ID is required')

            data = self.parser.parse_args()
            product_name = data['product_name']
            category_id = data['category_id']
            product_id = ProductModel.query.order_by(ProductModel.product_id.desc()).first().product_id + 1
            ProductModel.add_book_product(product_id, product_name, category_id)
            return res(message="Product added successfully")
        
        else:
            return res(success=False, message='Access denied.', code=403)


class Product(Resource):
    @jwt_required()
    def get(self, product_id, category_id):
        category = ProductModel.find_by_category_id(category_id)
        if not category:
            return res(success=False, message="Category not found", code=404)
        product = ProductModel.find_by_product_id(product_id)
        if product:
            book_product_list = ProductModel.find_all()
            result = []
            for book_product in book_product_list:
                result.append(book_product.dict())
            return res(data=result)
        return res(success=False, message="Product not found", code=404)

    @jwt_required()
    def delete(self, product_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            product = ProductModel.find_by_product_id(product_id)
            if product:
                ProductModel.delete_product_info(product_id)
                return res(message="Product deleted successfully")
            return res(success=False, message="Product not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)
    
    @jwt_required()
    def put(self, product_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':        
            data = self.parser.parse_args()
            product_name = data['product_name']
            category_id = data['category_id']
            product = ProductModel.find_by_product_id(product_id)
            if product:
                ProductModel.update(product_id, product_name, category_id)
                return res(message="Product updated successfully")
            return res(success=False, message="Product not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)
