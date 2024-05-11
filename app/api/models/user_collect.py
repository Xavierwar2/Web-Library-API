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
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    def dict(self):
        return {
            "collection_id": self.collection_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "created_at": format_datetime_to_json(self.created_at),
            "updated_at": format_datetime_to_json(self.updated_at),
        }

    # 新增一条记录
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 按 user_id 查找
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()

    # 按 collect_id 删除
    @classmethod
    def delete_by_collect_id(cls, collection_id):
        db.session.query(cls).filter_by(collection_id=collection_id).delete()
        db.session.commit()
