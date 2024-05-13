from datetime import datetime, timedelta
from ..models import db
from ..utils.format import format_datetime_to_json, format_date_to_json


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
    borrow_time = db.Column(db.Date, default=datetime.now, nullable=False)
    return_time = db.Column(db.Date, default=datetime.now() + timedelta(days=30), nullable=False)
    book_status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "borrow_id": self.borrow_id,
            "borrow_time": format_date_to_json(self.borrow_time),
            "return_time": format_date_to_json(self.return_time),
            "book_status": self.book_status,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "created_at": format_datetime_to_json(self.created_at),
            "updated_at": format_datetime_to_json(self.updated_at),
        }

    # 新增一条记录
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 返回所有记录
    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    # 根据borrow_id查找
    @classmethod
    def find_by_borrow_id(cls, borrow_id):
        return db.session.query(cls).get(borrow_id)

    # 按 user_id 查找
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()

    # 删除借阅项
    @classmethod
    def delete_by_borrow_id(cls, borrow_id):
        db.session.query(cls).filter_by(borrow_id=borrow_id).delete()
        db.session.commit()

    # 更新归还时间和书籍状态
    @classmethod
    def update_borrow_info(cls, borrow_info):
        update_data = {
            "return_time": borrow_info.return_time,
            "book_status": borrow_info.book_status,
        }
        db.session.query(cls).filter_by(borrow_id=borrow_info.borrow_id).update(update_data)
        db.session.commit()
