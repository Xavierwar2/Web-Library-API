from flask_restful import Resource, reqparse
from flask import request

from ..schema.email_verify_sha import email_verify_args_valid
from ..utils import redis_captcha
from ..utils.format import res
from ...extensions import mail
from flask_mail import Message
import random
import string


class Captcha(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        email_verify_args_valid(parser)
        data = parser.parse_args()
        mode = data['mode']
        email = data['email']

        # 生成验证码
        captcha = "".join(random.sample(string.digits * 4, 4))

        # 注册验证
        if mode == 0:
            message = Message(subject="您正在注册智能图书管理系统的账号！", recipients=[email],
                              body=f"您正在注册智能图书管理系统的账号，验证码是：{captcha}，请勿随意告知他人")
        # 登录验证
        elif mode == 1:
            message = Message(subject="您正在使用邮箱验证登录智能图书管理系统！", recipients=[email],
                              body=f"您正在使用邮箱验证登录智能图书管理系统，验证码是：{captcha}，请勿随意告知他人")

        else:
            return res(success=False, message='Invalid mode!', code=400)

        # 异常处理
        try:
            mail.send(message)
        except Exception as e:
            return res(success=False, message="Error: {}".format(e), code=500)

        # 验证码保存，一般有时效性，且频繁请求变化，所以保存在Redis中
        redis_captcha.redis_set(key=email, value=captcha)  # redis中都是键值对类型，存储验证码
        return res(message="Captcha has been successfully sent!")
