from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class BorrowModel(db.Model):
    """
    借阅信息表，根据用户id，在图书借阅表查询属于该用户的所有借阅书籍信息
    borrow_id   借阅id，主键
    user_id	用户id，外键
    book_id	书籍id，外键
    borrow_time	date	借出日期
    return_time	date	归还日期，若为null，则说明这次借阅还未完成
    book_status	int	书籍状态，默认为0（借阅中）
    """
    __tablename__ = "borrow_info"
    borrow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_time = db.Column(db.Date, default=datetime.now(), nullable=False)
    return_time = db.Column(db.Date)
    book_status = db.Column(db.Integer, default=0)
    username = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 字典
    def dict(self):
        return {
            "borrow_id": self.borrow_id,
            "borrow_time": self.borrow_time,
            "return_time": self.return_time,
            "book_status": self.book_status,
            "username": self.username,
            "book_name": self.book_name,
            "created_at": format_datetime_to_json(self.created_at),
            "updated_at": format_datetime_to_json(self.updated_at),
        }

    # 返回所有记录
    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()
