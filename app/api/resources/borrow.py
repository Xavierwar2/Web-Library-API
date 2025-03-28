from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from datetime import timedelta
from ..models.book_info import BookModel
from ..models.borrow_info import BorrowModel
from ..models.user_info import UserModel
from ..utils.format import res
from .base import BaseResource
from ..extensions import cache

class BorrowList(BaseResource):
    @jwt_required()
    @cache.cached(timeout=300, key_prefix='borrow_list')
    def get(self):
        """获取所有借阅信息"""
        @self.admin_required
        def get_all_borrows():
            try:
                borrow_info_list = BorrowModel.find_all()
                result = []
                for borrow_info in borrow_info_list:
                    result.append(self._format_borrow_info(borrow_info))
                return res(data=result)
            except Exception as e:
                return self.handle_error(e)
        return get_all_borrows()

    @jwt_required()
    def post(self):
        """创建新的借阅记录"""
        try:
            data = self._parse_borrow_args()
            user_info = self.validate_exists(UserModel, data['user_id'], 'user_id')
            book_info = self.validate_exists(BookModel, data['book_id'], 'book_id')

            if not book_info or not user_info:
                return res(success=False, message="Book or user not found", code=404)

            if book_info.current_number <= 0:
                return res(success=False, message="Book is not available for borrowing", code=400)

            borrow_info = BorrowModel(
                user_id=data['user_id'],
                book_id=data['book_id'],
            )
            borrow_info.add()

            # 更新图书状态
            book_info.borrow_count += 1
            book_info.current_number -= 1
            BookModel.update_book_info(book_info)
            
            # 清除缓存
            cache.delete('borrow_list')
            
            return res(message="Book borrowed successfully!")
        except Exception as e:
            return self.handle_error(e)

    def _parse_borrow_args(self):
        """解析借阅参数"""
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('book_id', type=int, required=True, help='Book ID is required')
        return parser.parse_args()

    def _format_borrow_info(self, borrow_info):
        """格式化借阅信息"""
        borrow_info_dict = borrow_info.dict()
        user_info = UserModel.find_by_user_id(borrow_info.user_id)
        book_info = BookModel.find_by_book_id(borrow_info.book_id)
        if book_info and user_info:
            borrow_info_dict.update({
                "username": user_info.username,
                "book_name": book_info.book_name
            })
        return borrow_info_dict


class Borrow(BaseResource):
    @jwt_required()
    @cache.memoize(300)
    def get(self, borrow_id):
        """获取单个借阅信息"""
        try:
            borrow_info = self.validate_exists(BorrowModel, borrow_id, 'borrow_id')
            if not borrow_info:
                return res(success=False, message="Borrow not found", code=404)
            return res(data=self._format_borrow_info(borrow_info))
        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def delete(self, borrow_id):
        """删除借阅记录"""
        @self.admin_required
        def delete_borrow():
            try:
                borrow_info = self.validate_exists(BorrowModel, borrow_id, 'borrow_id')
                if not borrow_info:
                    return res(success=False, message="Borrow information not found", code=404)

                book_info = self.validate_exists(BookModel, borrow_info.book_id, 'book_id')
                if not book_info:
                    return res(success=False, message="Book not found", code=404)

                BorrowModel.delete_by_borrow_id(borrow_id)
                
                # 清除缓存
                cache.delete_memoized(self.get, borrow_id)
                cache.delete('borrow_list')
                
                return res(message="Borrow information deleted successfully!")
            except Exception as e:
                return self.handle_error(e)
        return delete_borrow()

    @jwt_required()
    def put(self, borrow_id):
        """更新借阅状态"""
        @self.admin_required
        def update_borrow():
            try:
                data = self._parse_update_args()
                borrow_info = self.validate_exists(BorrowModel, borrow_id, 'borrow_id')
                if not borrow_info:
                    return res(success=False, message="Borrow information not found", code=404)

                if data['is_renew'] == 1:
                    return self._handle_renewal(borrow_info)
                elif data['book_status'] == 1:
                    return self._handle_return(borrow_info)
                
                return res(success=False, message="Invalid operation", code=400)
            except Exception as e:
                return self.handle_error(e)
        return update_borrow()

    def _parse_update_args(self):
        """解析更新参数"""
        parser = reqparse.RequestParser()
        parser.add_argument('book_status', type=int)
        parser.add_argument('is_renew', type=int)
        return parser.parse_args()

    def _handle_renewal(self, borrow_info):
        """处理续借"""
        borrow_info.return_time += timedelta(days=15)
        BorrowModel.update_borrow_info(borrow_info)
        cache.delete_memoized(self.get, borrow_info.borrow_id)
        return res(message="Return date updated successfully!")

    def _handle_return(self, borrow_info):
        """处理还书"""
        if borrow_info.book_status == 1:
            return res(success=False, message='Book is already returned!', code=400)

        book_info = self.validate_exists(BookModel, borrow_info.book_id, 'book_id')
        if not book_info:
            return res(success=False, message="Book not found", code=404)

        borrow_info.book_status = 1
        BorrowModel.update_borrow_info(borrow_info)
        book_info.current_number += 1
        BookModel.update_book_info(book_info)
        
        # 清除缓存
        cache.delete_memoized(self.get, borrow_info.borrow_id)
        cache.delete('borrow_list')
        
        return res(message="Return book status successfully!")

    def _format_borrow_info(self, borrow_info):
        """格式化借阅信息"""
        borrow_info_dict = borrow_info.dict()
        user_info = UserModel.find_by_user_id(borrow_info.user_id)
        book_info = BookModel.find_by_book_id(borrow_info.book_id)
        if book_info and user_info:
            borrow_info_dict.update({
                "username": user_info.username,
                "book_name": book_info.book_name
            })
        return borrow_info_dict


class BorrowByUser(BaseResource):
    @jwt_required()
    @cache.memoize(300)
    def get(self, user_id):
        """获取用户的所有借阅信息"""
        try:
            borrow_info_list = BorrowModel.find_by_user_id(user_id)
            result = []
            for borrow_info in borrow_info_list:
                result.append(self._format_borrow_info(borrow_info))
            return res(data=result)
        except Exception as e:
            return self.handle_error(e)

    def _format_borrow_info(self, borrow_info):
        """格式化借阅信息"""
        borrow_info_dict = borrow_info.dict()
        user_info = UserModel.find_by_user_id(borrow_info.user_id)
        book_info = BookModel.find_by_book_id(borrow_info.book_id)
        if book_info and user_info:
            borrow_info_dict.update({
                "username": user_info.username,
                "book_name": book_info.book_name
            })
        return borrow_info_dict
