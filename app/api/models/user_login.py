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
    #         "password": self.password,
    #         "salt": self.salt,
    #         "created_at": format_datetime_to_json(self.created_at),
    #         "updated_at": format_datetime_to_json(self.updated_at),
    #     }

    # 新增一条记录
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 按 username 查找
    @classmethod
    def find_by_username(cls, username):
        return db.session.execute(db.select(cls).filter_by(username=username)).first()
