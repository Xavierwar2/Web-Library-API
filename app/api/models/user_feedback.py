from datetime import datetime
from ..models import db
from ..common.utils import format_datetime_to_json


class FeedbackModel(db.Model):
    """
    le
    feedback_id	int	反馈id，主键
    user_id	int	用户id，外键
    message	text	信息
    """
    __tablename__ = "user_feedback"
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
