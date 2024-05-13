from datetime import datetime, timedelta

from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource
from ..models.book_info import BookModel
from ..models.borrow_info import BorrowModel

from ..utils.format import res


class Report(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']
        if role == 'admin':
            keys = ['title', 'tag', 'tagType', 'value', 'description']
            book_value = 0
            borrow_value = 0
            return_value = 0
            overdue_value = 0
            new_book_value = 0
            borrow_user_ids = set()
            return_user_ids = set()
            overdue_user_ids = set()

            book_info_list = BookModel.find_all()
            for book_info in book_info_list:
                # 图书总数
                book_value += book_info.number
                # 本周新增图书数
                if datetime.now() <= book_info.created_at + timedelta(days=7):
                    new_book_value += 1
                # 在借图书数
                borrow_value += (book_info.number - book_info.current_number)

            borrow_info_list = BorrowModel.find_all()
            for borrow_info in borrow_info_list:
                if borrow_info.book_status == 1:
                    borrow_user_ids.add(borrow_info.user_id)
                # 已还图书数
                if borrow_info.book_status == 1:
                    return_value += 1
                    return_user_ids.add(borrow_info.user_id)
                # 逾期未还数
                if datetime.now().date() > borrow_info.return_time:
                    overdue_value += 1
                    overdue_user_ids.add(borrow_info.user_id)

            borrow_user_value = len(borrow_user_ids)
            return_user_value = len(return_user_ids)
            overdue_user_value = len(overdue_user_ids)

            values = [['图书总数', '总', 'blue', book_value, f'本周新增 {new_book_value} 种'],
                      ['在借图书', '借', 'green', borrow_value, f'共 {borrow_user_value} 人'],
                      ['已还图书', '还', 'blue', return_value, f'共 {return_user_value} 人'],
                      ['逾期未还', '逾', 'green', overdue_value, f'共 {overdue_user_value} 人']]

            result = [dict(zip(keys, value)) for value in values]
            return res(data=result)
        else:
            return res(success=False, message="Role must be admin", code=403)

