from flask_restful import Resource, reqparse
from ..models.user_collect import CollectModel
from ..schema.collect_sha import user_collect_args_valid
from ..utils.format import res


class Collect(Resource):
    def get(self, user_id):
        collect_info_list = CollectModel.find_by_user_id(user_id)
        result = []
        for collect_info in collect_info_list:
            result.append(collect_info.dict())

        return res(data=result)

    def post(self):
        parser = reqparse.RequestParser()
        user_collect_args_valid(parser)
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

    def delete(self, collection_id):
        try:
            CollectModel.delete_by_collect_id(collection_id)
            return res(message='Book deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)