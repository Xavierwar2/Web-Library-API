from datetime import datetime
from ..utils.format import format_datetime_to_json
from ..models import db


class UserModel(db.Model):
    """
    用户信息表，用于存储用户信息（不存储用户密码）
    """

    __tablename__ = "user_info"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True)
    sex = db.Column(db.Integer, default=2)
    age = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text,
                          default="https://tse2-mm.cn.bing.net/th/id/OIP-C.jHUH4s7TQ4…ozuJgHaHa?w=188&h=188&c=7&r=0&o"
                                  "=5&dpr=1.3&pid=1.7", nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now,
                           comment='更新时间')

    # 字典
    def dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "sex": self.sex,
            "age": self.age,
            "status": self.status,
            "image_url": self.image_url,
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

    # 按 user_id 查找
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls).get(user_id)

    # 按 username 查找
    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    # 按 email 查找
    @classmethod
    def find_by_email(cls, email):
        return db.session.execute(db.select(cls).filter_by(email=email)).first()

    # 按 user_id 删除
    @classmethod
    def delete_by_user_id(cls, user_id):
        db.session.query(cls).filter_by(user_id=user_id).delete()
        db.session.commit()

    # 按 user_id 修改
    @classmethod
    def update_user(cls, user_id, username, email, sex, age, status, image_url):
        update_data = {
            'username': username,
            'email': email,
            'sex': sex,
            'age': age,
            'status': status,
            'image_url': image_url,
        }
        db.session.query(cls).filter_by(user_id=user_id).update(update_data)
        db.session.commit()
