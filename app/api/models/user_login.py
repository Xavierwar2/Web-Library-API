from datetime import datetime
from ..models import db
from ..utils.format import format_datetime_to_json


class UserLoginModel(db.Model):
    """
    用户端登陆信息表，用于验证登录信息
    """
    __tablename__ = "user_login"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), comment='salt')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # # 字典
    # def dict(self):
    #     return {
    #         "user_id": self.user_id,
    #         "username": self.username,
    #         "created_at": format_datetime_to_json(self.created_at),
    #         "updated_at": format_datetime_to_json(self.updated_at),
    #     }

    # 新增一条记录
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 按 user_id 查找
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls).get(user_id)

    # 按 username 查找
    @classmethod
    def find_by_username(cls, username):
        return db.session.execute(db.select(cls).filter_by(username=username)).first()

    # 按 user_id 删除
    @classmethod
    def delete_by_user_id(cls, user_id):
        db.session.query(cls).filter_by(user_id=user_id).delete()
        db.session.commit()

    # 按 user_id 修改
    @classmethod
    def update_user(cls, user_id, username, password, salt):
        update_data = {
            "username": username,
            "password": password,
            "salt": salt,
        }
        db.session.query(cls).filter_by(user_id=user_id).update(update_data)
        db.session.commit()
