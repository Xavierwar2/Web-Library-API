from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.book_info import BookModel
from datetime import datetime
from ..models.borrow_info import BorrowModel
from ..utils.format import res


class BorrowService(Resource):
    @jwt_required()
    def get(self):
        borrow_info_list = BorrowModel.find_all()
        result = []
        for borrow_info in borrow_info_list:
            result.append(borrow_info.dict())

        return res(data=result)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('book_id', type=int, required=True, help='Book ID is required')
        data = parser.parse_args()

        try:
            book = BookModel.find_by_id(data['book_id'])
            if not book:
                return res(success=False, message="Book not found", code=404)

            if book.current_number <= 0:
                return res(success=False, message="Book is not available for borrowing", code=400)

            borrow_info = BorrowModel(
                user_id=data['user_id'],
                book_id=data['book_id'],
                borrow_date=datetime.now(),
                return_date=None
            )
            borrow_info.save()

            # Update book status
            book.current_number -= 1
            book.save()

            return res(message="Book borrowed successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('borrow_id', type=int, required=True, help='Borrow ID is required')
        data = parser.parse_args()

        try:
            borrow_info = BorrowModel.find_by_id(data['borrow_id'])
            if not borrow_info:
                return res(success=False, message="Borrow information not found", code=404)

            book = BookModel.find_by_id(borrow_info.book_id)
            if not book:
                return res(success=False, message="Book not found", code=404)

            # Update book status
            book.current_number += 1
            book.save()

            borrow_info.delete()

            return res(message="Borrow information deleted successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('borrow_id', type=int, required=True, help='Borrow ID is required')
        parser.add_argument('return_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Return date is required')
        data = parser.parse_args()

        try:
            borrow_info = BorrowModel.find_by_id(data['borrow_id'])
            if not borrow_info:
                return res(success=False, message="Borrow information not found", code=404)

            borrow_info.return_date = data['return_date']
            borrow_info.save()

            # Update book status
            book = BookModel.find_by_id(borrow_info.book_id)
            if not book:
                return res(success=False, message="Book not found", code=404)

            book.current_number += 1
            book.save()

            return res(message="Return date updated successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

    @jwt_required()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('borrow_id', type=int, required=True, help='Borrow ID is required')
        parser.add_argument('return_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Return date is required')
        data = parser.parse_args()

        try:
            borrow_info = BorrowModel.find_by_id(data['borrow_id'])
            if not borrow_info:
                return res(success=False, message="Borrow information not found", code=404)

            borrow_info.return_date = data['return_date']
            borrow_info.save()

            return res(message="Return date updated successfully!")
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)
