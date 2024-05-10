from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


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
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "category_id": self.category_id,
            "created_at": format_datetime_to_json(self.created_at),
            "updated_at": format_datetime_to_json(self.created_at),

        }

    # 返回所有记录
    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    # 按product_id查找
    @classmethod
    def find_by_product_id(cls, product_id):
        return db.session.execute(db.select(cls).filter_by(product_id=product_id)).first()

    # 按category_id查找
    @classmethod
    def find_by_category_id(cls, category_id):
        return db.session.execute(db.select(cls).filter_by(category_id=category_id)).first()

    # 新增一条记录
    @classmethod
    def add_book_product(cls, product_id, product_name, category_id):
        book_product = cls(
            product_id=product_id,
            product_name=product_name,
            category_id=category_id
        )
        db.session.add(book_product)
        db.session.commit()

    #  删除一项记录
    @classmethod
    def delete_product_info(cls, product_id):
        product_info = cls.query.get(product_id)
        if product_info:
            db.session.delete(product_id)
            db.session.commit()

    # 更新表格
    @classmethod
    def update(cls, product_id, product_name, category_id):
        update_date = {
            'product_id': product_id,
            "product_name": product_name,
            'category_id': category_id
        }
        db.session.query(cls).filter_by(product_id=product_id).update(update_date)
        db.session.commit()
