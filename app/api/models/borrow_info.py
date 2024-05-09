from datetime import datetime
from ..models import db
from ..common.utils import format_datetime_to_json


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
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
