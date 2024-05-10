from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.book_info import BookModel
from datetime import datetime
from ..models.book_product import ProductModel
from ..utils.format import res


class ProductService(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
    parser.add_argument('product_name', type=str, required=True, help='Product name is required')
    parser.add_argument('category_id', type=int, required=True, help='Category ID is required')

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
        return res(message="Product not found", status=404)

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        product_name = data['product_name']
        category_id = data['category_id']
        product_id = ProductModel.query.order_by(ProductModel.product_id.desc()).first().product_id + 1
        ProductModel.add_book_product(product_id, product_name, category_id)
        return res(message="Product added successfully", status=201)

    @jwt_required()
    def put(self, product_id):
        data = self.parser.parse_args()
        product_name = data['product_name']
        category_id = data['category_id']
        product = ProductModel.find_by_product_id(product_id)
        if product:
            ProductModel.update(product_id, product_name, category_id)
            return res(message="Product updated successfully")
        return res(message="Product not found", status=404)

    @jwt_required()
    def delete(self, product_id):
        product = ProductModel.find_by_product_id(product_id)
        if product:
            ProductModel.delete_product_info(product_id)
            return res(message="Product deleted successfully")
        return res(message="Product not found", status=404)

