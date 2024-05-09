from datetime import datetime
from ..models import db
from ..common.utils import format_datetime_to_json


class ProductModel(db.Model):
    """
    product_id	int	图书小类别id，主键
    product_name	varchar(20)	图书小类别名称，不超过20个字符，不能为空
    category	int	图书大类别id，外键

    """
    __tablename__ = "book_product"
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(20), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
