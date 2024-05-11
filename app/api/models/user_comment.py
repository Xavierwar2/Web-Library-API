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
