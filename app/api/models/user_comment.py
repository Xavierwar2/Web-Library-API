from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class CommentModel(db.Model):
    """
    评论信息表
    """
    __tablename__ = "user_comment"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "comment_id": self.comment_id,
            "content": self.content,
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

    # 按 comment_id 查找
    @classmethod
    def find_by_comment_id(cls, comment_id):
        return db.session.query(cls).get(comment_id)

    # 按 book_id 查找
    @classmethod
    def find_by_book_id(cls, book_id):
        return db.session.query(cls).filter_by(book_id=book_id).all()

    # 按 user_id 查找
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()

    # 按 comment_id 删除
    @classmethod
    def delete_by_comment_id(cls, comment_id):
        db.session.query(cls).filter_by(comment_id=comment_id).delete()
        db.session.commit()

    # 按 comment_id 修改
    @classmethod
    def update_comment(cls, comment_id, content):
        update_data = {
            "content": content,
        }
        db.session.query(cls).filter_by(comment_id=comment_id).update(update_data)
        db.session.commit()
