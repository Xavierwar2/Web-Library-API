from datetime import datetime
from ..models import db
from ..common.utils import format_datetime_to_json


class CategoryModel(db.Model):
    """
    category_id	int	图书大类别id，主键
    category_name	varchar(20)	图书大类别名称，不超过20个字符，不能为空

    """
    __tablename__ = "book_category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
