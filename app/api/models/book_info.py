from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class BookModel(db.Model):
    """
    图书信息表，用于存储图书信息
    book_id:图书id，主键
    book_name	varchar(50)	图书名称，不能为空
    author	varchar(50)	作者，默认为佚名
    text	text	图书简介，不超过50字，默认为暂无简介
    image_url	text	图书图片链接，默认为默认图片链接
    borrow_count	int	图书被借阅次数，默认为0
    current_number	int	现存数量，默认为0
    number	int	库存总数，默认为0
    category_id	int	图书所属大类别，外键
    product_id	int	图书所属小类别，外键

    """
    __tablename__ = "book_info"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), default="佚名")
    text = db.Column(db.Text, default="暂无简介", nullable=False)
    image_url = db.Column(db.Text,
                          default="https://tse2-mm.cn.bing.net/th/id/OIP-C.jHUH4s7TQ4…ozuJgHaHa?w=188&h=188&c=7&r=0&o"
                                  "=5&dpr=1.3&pid=1.7", nullable=False)
    borrow_count = db.Column(db.Integer, default=0)
    current_number = db.Column(db.Integer, default=0)
    number = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
