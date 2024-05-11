from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.user_comment import CommentModel
from ..schema.comment_sha import comment_args_valid
from ..utils.format import res


class CommentList(Resource):
    @jwt_required()
    def get(self):
        user_comment_list = CommentModel.find_all()
        result = []
        for user_comment in user_comment_list:
            result.append(user_comment.dict())

        return res(data=result)

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


class Comment(Resource):
    @jwt_required()
    def get(self, comment_id):
        user_comment = CommentModel.find_by_comment_id(comment_id)
        if user_comment:
            return res(data=user_comment.dict())
        else:
            return res(message="Comment not found", code=404)

    @jwt_required()
    def delete(self, comment_id):
        try:
            CommentModel.delete_by_comment_id(comment_id)
            return res(message='Comment deleted successfully!')
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def put(self, comment_id):
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
