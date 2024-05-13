import io
import json
from datetime import datetime

import qrcode
from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


# Flask-Restful资源
from app.api.utils.format import format_datetime_to_json


class QRCode(Resource):

    @jwt_required()
    def get(self):
        # 获取数据
        user_id = request.args.get('user_id')
        book_id = request.args.get('book_id')
        timestamp = format_datetime_to_json(datetime.now())
        text_dict = {'user_id': user_id, 'book_id': book_id, "timestamp": timestamp}
        text = json.dumps(text_dict)
        im = qrcode.make(text)  # 生成二维码
        img = io.BytesIO()  # 创建图片流
        im.save(img, format='PNG')  # 将图片放图片流里面
        img = img.getvalue()  # 返回图片流
        return Response(img, mimetype='image/png')  # 用自定义返回的数据及类型
