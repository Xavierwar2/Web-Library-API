from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from ..models.user_collect import CollectModel
from ..schema.collect_sha import collect_args_valid
from ..models.book_info import BookModel
from ..models.user_info import UserModel
from ..utils.format import res


class Collect(Resource):
    @jwt_required()
    def get(self, user_id):
        user_collect_list = CollectModel.find_by_user_id(user_id)
        result = []
        for user_collect in user_collect_list:
            user_collect_dict = user_collect.dict()
            user_id = user_collect.user_id
            book_id = user_collect.book_id
            book_info = BookModel.find_by_book_id(book_id)
            user_info = UserModel.find_by_user_id(user_id)
            if book_info and user_info:
                user_collect_dict.update({"username": user_info.username})
                user_collect_dict.update({"book_name": book_info.book_name})
            result.append(user_collect_dict)

        return res(data=result)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        collect_args_valid(parser)
        data = parser.parse_args()
        try:
            user_id = data['user_id']
            book_id = data['book_id']
            collect_info_list = CollectModel.find_by_user_id(user_id)
            for collect_info in collect_info_list:
                if collect_info.book_id == book_id:
                    return res(success=False, message="You have already collected this book", code=500)
            collect_info = CollectModel(user_id=user_id, book_id=book_id)
            collect_info.add()
            return res(message="Collect Book successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def delete(self, collection_id):
        try:
            CollectModel.delete_by_collection_id(collection_id)
            return res(message='Collection deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)


class CollectList(Resource):
    @jwt_required()
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            collect_args_valid(parser)
            data = parser.parse_args()
            delete_list = data['delete_list']
            # 根据提供的 ID 数组执行删除操作
            for collect in delete_list:
                collection_id = collect.get('collection_id')
                CollectModel.delete_by_collection_id(collection_id)
            return res(message='Collects deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)
