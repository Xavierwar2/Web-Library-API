from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from ..models.user_comment import CommentModel
from ..models.user_info import UserModel
from ..models.book_info import BookModel
from ..schema.comment_sha import comment_args_valid
from ..utils.format import res
from ..models.user_info import UserModel
from ..models.book_info import BookModel


class CommentList(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            user_comment_list = CommentModel.find_all()
            result = []
            for user_comment in user_comment_list:
                user_comment_dict = user_comment.dict()
                user_id = user_comment.user_id
                book_id = user_comment.book_id
                book_info = BookModel.find_by_book_id(book_id)
                user_info = UserModel.find_by_user_id(user_id)
                user_comment_dict.update({"username": user_info.username})
                user_comment_dict.update({"book_name": book_info.book_name})
                result.append(user_comment_dict)
            return res(data=result)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        comment_args_valid(parser)
        data = parser.parse_args()
        try:
            content = data['content']
            user_id = data['user_id']
            book_id = data['book_id']
            user_comment = CommentModel(content=content, user_id=user_id,
                                        book_id=book_id)
            user_comment.add()
            return res(message="Add Comment successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def delete(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                parser = reqparse.RequestParser()
                comment_args_valid(parser)
                data = parser.parse_args()
                delete_list = data['delete_list']
                # 根据提供的 ID 数组执行删除操作
                for comment in delete_list:
                    comment_id = comment.get('comment_id')
                    CommentModel.delete_by_comment_id(comment_id)
                return res(message='Comment deleted successfully!')

            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class Comment(Resource):
    @jwt_required()
    def get(self, comment_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            user_comment = CommentModel.find_by_comment_id(comment_id)
            if user_comment:
                user_comment_dict = user_comment.dict()
                user_id = user_comment.user_id
                book_id = user_comment.book_id
                book_info = BookModel.find_by_book_id(book_id)
                user_info = UserModel.find_by_user_id(user_id)
                user_comment_dict.update({"username": user_info.username})
                user_comment_dict.update({"book_name": book_info.book_name})
                return res(data=user_comment_dict)
            else:
                return res(message="Comment not found", code=404)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def delete(self, comment_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                CommentModel.delete_by_comment_id(comment_id)
                return res(message='Comment deleted successfully!')
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def put(self, comment_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            comment_args_valid(parser)
            data = parser.parse_args()
            try:
                user_comment = CommentModel.find_by_comment_id(comment_id)
                if user_comment:
                    content = data['content']
                    user_comment.update_comment(comment_id, content)
                    return res(message="Update comment successfully!")
                else:
                    return res(success=False, message="Comment not found", code=404)
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)


class CommentByUser(Resource):
    @jwt_required()
    def get(self, user_id):
        user_comment_list = CommentModel.find_by_user_id(user_id)
        result = []
        for user_comment in user_comment_list:
            result.append(user_comment.dict())

        return res(data=result)


class CommentByBook(Resource):
    def get(self, book_id):
        user_comment_list = CommentModel.find_by_book_id(book_id)
        result = []
        for user_comment in user_comment_list:
            result.append(user_comment.dict())

        return res(data=result)
