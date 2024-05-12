from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class CategoryModel(db.Model):
    """
    category_id	int	图书大类别id，主键
    category_name	varchar(20)	图书大类别名称，不超过20个字符，不能为空

    """
    __tablename__ = "book_category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "created_at": format_datetime_to_json(self.created_at),
            "updated_at": format_datetime_to_json(self.created_at),

        }

    # 返回所有记录
    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    # 按category_id查找
    @classmethod
    def find_by_category_id(cls, category_id):
        return db.session.execute(db.select(cls).filter_by(category_id=category_id)).first()

    # 新增一条记录
    @classmethod
    def add_book_category(cls, category_name):
        book_category = cls(
            category_name=category_name
        )
        db.session.add(book_category)
        db.session.commit()

    #  删除一项记录
    @classmethod
    def delete_category_info(cls, category_id):
        category_info = cls.query.get(category_id)
        if category_info:
            db.session.delete(category_id)
            db.session.commit()
    # 更新表格
    @classmethod
    def update(cls, category_id, category_name):
        update_date = {
            'category_id': category_id,
            "category_name": category_name
        }
        db.session.query(cls).filter_by(category_id=category_id).update(update_date)
        db.session.commit()
