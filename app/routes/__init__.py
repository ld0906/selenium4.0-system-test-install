"""
主路由模块
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Menu, db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页 - 重定向到系统主页或登录页"""
    if current_user.is_authenticated:
        return redirect(url_for('main.system_index'))
    return redirect(url_for('auth.login'))


@main_bp.route('/index')
@login_required
def system_index():
    """系统主页框架"""
    # 获取当前用户的菜单
    menus = get_user_menus(current_user)
    
    return render_template('index.html',
                         user=current_user,
                         menus=menus,
                         isMobile=is_mobile_device())


@main_bp.route('/system/main')
@login_required
def main_content():
    """系统主页内容"""
    return render_template('main.html', user=current_user)


def get_user_menus(user):
    """
    获取用户菜单
    返回树形结构的菜单列表
    """
    if user.is_admin():
        # 管理员获取所有菜单
        all_menus = Menu.query.filter_by(
            visible='0'
        ).filter(
            Menu.menu_type.in_(['M', 'C'])
        ).order_by(
            Menu.parent_id, Menu.order_num
        ).all()
    else:
        # 普通用户根据角色获取菜单
        menu_ids = set()
        for role in user.roles:
            if role.status == '0':  # 角色正常状态
                for menu in role.menus:
                    if menu.visible == '0' and menu.menu_type in ['M', 'C']:
                        menu_ids.add(menu.menu_id)
        
        if not menu_ids:
            return []
        
        all_menus = Menu.query.filter(
            Menu.menu_id.in_(menu_ids)
        ).order_by(
            Menu.parent_id, Menu.order_num
        ).all()
    
    # 转换为字典列表
    menu_list = []
    for menu in all_menus:
        menu_dict = {
            'menu_id': menu.menu_id,
            'menu_name': menu.menu_name,
            'parent_id': menu.parent_id,
            'order_num': menu.order_num,
            'url': menu.url,
            'target': menu.target,
            'menu_type': menu.menu_type,
            'visible': menu.visible,
            'is_refresh': menu.is_refresh,
            'perms': menu.perms,
            'icon': menu.icon
        }
        menu_list.append(menu_dict)
    
    # 构建树形结构
    return build_menu_tree(menu_list)


def build_menu_tree(menu_list, parent_id=0):
    """构建菜单树"""
    tree = []
    for menu in menu_list:
        if menu['parent_id'] == parent_id:
            children = build_menu_tree(menu_list, menu['menu_id'])
            if children:
                menu['children'] = children
            tree.append(menu)
    return tree


def is_mobile_device():
    """检测是否是移动设备"""
    from flask import request
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'phone']
    return any(keyword in user_agent for keyword in mobile_keywords)
