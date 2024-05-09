from flask_restful import Resource
from flask_jwt_extended import jwt_required
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
