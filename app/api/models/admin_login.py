from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class AdminLoginModel(db.Model):
    """
    后台登陆信息表，用于验证登录信息及权限
    """
    __tablename__ = "admin_login"
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), comment='salt')
    is_super_admin = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 字典
    def dict(self):
        return {
            "admin_id": self.admin_id,
            "username": self.username,
            "is_super_admin": self.is_super_admin,
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

    # 按 admin_id 查找
    @classmethod
    def find_by_admin_id(cls, admin_id):
        return db.session.query(cls).get(admin_id)

    # 按 username 查找
    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    # 按 admin_id 删除
    @classmethod
    def delete_by_admin_id(cls, admin_id):
        db.session.query(cls).filter_by(admin_id=admin_id).delete()
        db.session.commit()

    # 按 admin_id 修改
    @classmethod
    def update_admin(cls, admin_id, username, password, salt, is_super_admin):
        update_data = {
            "username": username,
            "password": password,
            "salt": salt,
            "is_super_admin": is_super_admin,
        }
        db.session.query(cls).filter_by(admin_id=admin_id).update(update_data)
        db.session.commit()
