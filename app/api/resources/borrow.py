from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from ..models.book_info import BookModel
from datetime import datetime, timedelta
from ..models.borrow_info import BorrowModel
from ..utils.format import res
from ..models.user_info import UserModel


class BorrowList(Resource):
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            borrow_info_list = BorrowModel.find_all()
            result = []
            for borrow_info in borrow_info_list:
                result.append(borrow_info.dict())

            return res(data=result)

        else:
            return res(success=False, message='Access denied.', code=403)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('book_id', type=int, required=True, help='Book ID is required')
        data = parser.parse_args()

        try:
            user_info = UserModel.find_by_user_id(data['user_id'])
            book_info = BookModel.find_by_book_id(data['book_id'])
            if not book_info:
                return res(success=False, message="Book not found", code=404)

            if not user_info:
                return res(success=False, message="User not found", code=404)

            if book_info.current_number <= 0:
                return res(success=False, message="Book is not available for borrowing", code=400)

            borrow_info = BorrowModel(
                user_id=data['user_id'],
                book_id=data['book_id'],
            )
            borrow_info.add()

            # Update book status
            book_info.borrow_count += 1
            book_info.current_number -= 1
            BookModel.update_book_info(book_info)

            return res(message="Book borrowed successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)


class Borrow(Resource):
    @jwt_required()
    def get(self, borrow_id):
        borrow_info = BorrowModel.find_by_borrow_id(borrow_id)
        if borrow_info:
            return res(data=borrow_info.dict())
        else:
            return res(message="Borrow not found", code=404)

    @jwt_required()
    def delete(self, borrow_id):
        jwt_data = get_jwt()
        role = jwt_data['role']

        # 管理员可以执行该操作
        if role == 'admin':
            try:
                borrow_info = BorrowModel.find_by_borrow_id(borrow_id)
                if not borrow_info:
                    return res(success=False, message="Borrow information not found", code=404)

                book_info = BookModel.find_by_book_id(borrow_info.book_id)
                if not book_info:
                    return res(success=False, message="Book not found", code=404)

                BorrowModel.delete_by_borrow_id(borrow_id)

                return res(message="Borrow information deleted successfully!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

        else:
            return res(success=False, message='Access denied.', code=403)

    # 这部分还没改完
    @jwt_required()
    def put(self, borrow_id):
        parser = reqparse.RequestParser()
        parser.add_argument('return_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                            help='Return date is required')
        data = parser.parse_args()

        try:
            borrow_info = BorrowModel.find_by_borrow_id(borrow_id)
            if not borrow_info:
                return res(success=False, message="Borrow information not found", code=404)

            if data['return_date']:
                borrow_info.return_date = data['return_date']

            borrow_info.book_status = 1
            BorrowModel.update(borrow_info)

            # Update book status
            book_info = BookModel.find_by_id(borrow_info.book_id)
            if not book_info:
                return res(success=False, message="Book not found", code=404)

            book_info.current_number += 1
            BookModel.update_book_info(book_info)

            return res(message="Return date updated successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)
