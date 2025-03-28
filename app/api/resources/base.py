from flask_restful import Resource
from flask_jwt_extended import get_jwt
from ..utils.format import res
from ..extensions import cache

class BaseResource(Resource):
    def check_admin_access(self):
        """检查是否具有管理员权限"""
        jwt_data = get_jwt()
        role = jwt_data.get('role')
        if role != 'admin':
            return False
        return True

    def admin_required(self, func):
        """管理员权限装饰器"""
        def wrapper(*args, **kwargs):
            if not self.check_admin_access():
                return res(success=False, message='Access denied.', code=403)
            return func(*args, **kwargs)
        return wrapper

    def handle_error(self, e):
        """统一错误处理"""
        return res(success=False, message=str(e), code=500)

    def validate_exists(self, model, id_value, id_field):
        """验证记录是否存在"""
        item = model.query.filter_by(**{id_field: id_value}).first()
        if not item:
            return None
        return item 