"""
工具函数模块
"""
import re
import hashlib
from datetime import datetime
from functools import wraps
from flask import request, jsonify
from flask_login import current_user
from app.models import DictData


def get_client_ip():
    """获取客户端IP地址"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def get_user_agent():
    """获取用户代理信息"""
    return request.headers.get('User-Agent', '')


def parse_user_agent(ua_string):
    """解析用户代理字符串，返回浏览器和操作系统信息"""
    browser = 'Unknown'
    os = 'Unknown'
    
    # 检测浏览器
    if 'Edge' in ua_string:
        browser = 'Edge'
    elif 'Chrome' in ua_string:
        browser = 'Chrome'
    elif 'Safari' in ua_string:
        browser = 'Safari'
    elif 'Firefox' in ua_string:
        browser = 'Firefox'
    elif 'MSIE' in ua_string or 'Trident' in ua_string:
        browser = 'IE'
    
    # 检测操作系统
    if 'Windows' in ua_string:
        os = 'Windows'
    elif 'Mac' in ua_string:
        os = 'macOS'
    elif 'Linux' in ua_string:
        os = 'Linux'
    elif 'Android' in ua_string:
        os = 'Android'
    elif 'iOS' in ua_string or 'iPhone' in ua_string or 'iPad' in ua_string:
        os = 'iOS'
    
    return browser, os


def get_dict_label(dict_type, dict_value):
    """根据字典类型和值获取标签"""
    if not dict_value:
        return ''
    dict_data = DictData.query.filter_by(
        dict_type=dict_type,
        dict_value=str(dict_value),
        status='0'
    ).first()
    return dict_data.dict_label if dict_data else dict_value


def get_dict_list(dict_type):
    """获取字典数据列表"""
    return DictData.query.filter_by(
        dict_type=dict_type,
        status='0'
    ).order_by(DictData.dict_sort).all()


def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间"""
    if not value:
        return ''
    if isinstance(value, str):
        return value
    return value.strftime(format)


def success_response(msg='操作成功', **kwargs):
    """成功响应"""
    result = {'code': 0, 'msg': msg}
    result.update(kwargs)
    return jsonify(result)


def error_response(msg='操作失败', code=500, **kwargs):
    """错误响应"""
    result = {'code': code, 'msg': msg}
    result.update(kwargs)
    return jsonify(result)


def table_response(rows, total=None):
    """表格数据响应"""
    if total is None:
        total = len(rows) if isinstance(rows, list) else rows.count()
    
    return jsonify({
        'code': 0,
        'msg': '查询成功',
        'rows': rows if isinstance(rows, list) else [item.to_dict() for item in rows],
        'total': total
    })


def paginate(query, page, per_page):
    """分页查询"""
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return pagination.items, pagination.total


def has_permission(permission):
    """检查当前用户是否有指定权限"""
    if not current_user.is_authenticated:
        return False
    return current_user.has_permission(permission)


def build_tree(items, parent_id=0, id_field='id', parent_field='parent_id', children_field='children'):
    """
    构建树形结构
    :param items: 数据列表(字典列表)
    :param parent_id: 父节点ID
    :param id_field: ID字段名
    :param parent_field: 父ID字段名
    :param children_field: 子节点字段名
    :return: 树形结构列表
    """
    tree = []
    for item in items:
        if item.get(parent_field) == parent_id:
            children = build_tree(items, item[id_field], id_field, parent_field, children_field)
            if children:
                item[children_field] = children
            tree.append(item)
    return tree


def validate_password(password):
    """
    验证密码强度
    返回: (is_valid, message)
    """
    if len(password) < 6:
        return False, '密码长度不能少于6个字符'
    if len(password) > 20:
        return False, '密码长度不能超过20个字符'
    
    # 可以根据需要添加更多验证规则
    # if not re.search(r'[A-Z]', password):
    #     return False, '密码必须包含大写字母'
    # if not re.search(r'[a-z]', password):
    #     return False, '密码必须包含小写字母'
    # if not re.search(r'[0-9]', password):
    #     return False, '密码必须包含数字'
    
    return True, '密码符合要求'


def validate_phone(phone):
    """验证手机号"""
    if not phone:
        return True, ''
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        return False, '手机号格式不正确'
    return True, ''


def validate_email(email):
    """验证邮箱"""
    if not email:
        return True, ''
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, '邮箱格式不正确'
    return True, ''


def generate_session_id():
    """生成会话ID"""
    import uuid
    return str(uuid.uuid4())


def get_ancestors(dept_id, dept_dict):
    """
    获取部门祖级列表
    :param dept_id: 部门ID
    :param dept_dict: 部门字典 {dept_id: dept}
    :return: 祖级字符串，如 "0,100,101"
    """
    ancestors = []
    current_id = dept_id
    
    while current_id and current_id in dept_dict:
        dept = dept_dict[current_id]
        parent_id = dept.get('parent_id', 0)
        if parent_id:
            ancestors.insert(0, str(parent_id))
        current_id = parent_id
    
    return ','.join(ancestors) if ancestors else '0'


def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def secure_filename(filename):
    """
    生成安全的文件名
    """
    import os
    from werkzeug.utils import secure_filename as werkzeug_secure
    
    # 获取文件扩展名
    ext = ''
    if '.' in filename:
        ext = '.' + filename.rsplit('.', 1)[1].lower()
    
    # 生成唯一文件名
    unique_name = hashlib.md5(
        f"{filename}{datetime.now().timestamp()}".encode()
    ).hexdigest()
    
    return unique_name + ext
