"""
权限装饰器
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def login_required(f):
    """需要登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录系统', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission):
    """
    需要指定权限
    用法: @permission_required('system:user:list')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """需要管理员权限"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def check_demo_mode(f):
    """演示模式检查(演示模式下某些操作会被限制)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import current_app, jsonify, request
        
        # 如果是POST/PUT/DELETE请求且开启了演示模式
        if request.method in ['POST', 'PUT', 'DELETE'] and current_app.config.get('DEMO_ENABLED'):
            # 可以在这里添加演示模式的限制逻辑
            # return jsonify({'code': 500, 'msg': '演示模式，不允许操作'})
            pass
        
        return f(*args, **kwargs)
    return decorated_function
