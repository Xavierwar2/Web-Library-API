from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from ..models.notice_info import NoticeModel
from ..schema.notice_sha import notice_args_valid
from ..utils.format import res


class NoticeList(Resource):
    def get(self):
        notice_info_list = NoticeModel.find_all()
        result = []
        for notice_info in notice_info_list:
            notice_info_dict = notice_info.dict()

            result.append(notice_info_dict)
        return res(data=result)

    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            parser = reqparse.RequestParser()
            notice_args_valid(parser)
            data = parser.parse_args()
            try:
                title = data['title']
                content = data['content']
                notice_info = NoticeModel(title=title, content=content)
                notice_info.add()
                return res(message="Add Notice successfully!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)
