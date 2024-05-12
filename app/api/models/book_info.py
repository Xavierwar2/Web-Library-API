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
    category_id = db.Column(db.Integer, nullable=False, default=0)
    product_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "book_id": self.book_id,
            "book_name": self.book_name,
            "author": self.author,
            "text": self.text,
            "image_url": self.image_url,
            "borrow_count": self.borrow_count,
            "current_number": self.current_number,
            "number": self.number,
            "category_id": self.category_id,
            "product_id": self.product_id,
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

    # 按 book_name 查找
    @classmethod
    def find_by_book_name(cls, book_name):
        return db.session.execute(db.select(cls).filter_by(book_name=book_name)).first()

    # 按 book_id 查找
    @classmethod
    def find_by_book_id(cls, book_id):
        return db.session.query(cls).get(book_id)

    # 按照 category 查找
    @classmethod
    def find_by_category_id(cls, category_id):
        return db.session.query(cls).filter_by(category_id=category_id).all()

    # 按 book_id 删除
    @classmethod
    def delete_by_book_id(cls, book_id):
        db.session.query(cls).filter_by(book_id=book_id).delete()
        db.session.commit()

    # 按 book_id 修改
    @classmethod
    def update_book_info(cls, book_info):
        update_data = {
            'book_name': book_info.book_name,
            'author': book_info.author,
            'text': book_info.text,
            'image_url': book_info.image_url,
            'current_number': book_info.current_number,
            'number': book_info.number,
            'category_id': book_info.category_id,
            'product_id': book_info.product_id
        }
        db.session.query(cls).filter_by(book_id=book_info.book_id).update(update_data)
        db.session.commit()

    # 按 book_id 修改 category_id
    @classmethod
    def update_book_category_id(cls, book_id, category_id):
        db.session.query(cls).filter_by(book_id=book_id).update(category_id=category_id)
        db.session.commit()
