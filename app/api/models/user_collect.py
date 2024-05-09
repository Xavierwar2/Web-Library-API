from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class CollectModel(db.Model):
    """
    用户收藏表，存储所有用户的收藏表单
    collection_id:收藏id，主键
    user_id:用户id，外键
    book_id:书籍id，外键
    """
    __tablename__ = "user_collect"
    collection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
