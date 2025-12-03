"""
系统管理路由 - 用户、角色、菜单、部门等管理
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Role, Menu, Dept, Post, DictType, DictData, Config, Notice
from app.decorators import permission_required
from app.utils import success_response, error_response, table_response, paginate, get_dict_list
from datetime import datetime

system_bp = Blueprint('system', __name__)


@system_bp.route('/user/list')
@login_required
@permission_required('system:user:view')
def user_list():
    """用户列表页面"""
    return render_template('system/user/user.html')


@system_bp.route('/user/list/data')
@login_required
@permission_required('system:user:list')
def user_list_data():
    """用户列表数据API"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    login_name = request.args.get('loginName', '').strip()
    phonenumber = request.args.get('phonenumber', '').strip()
    status = request.args.get('status', '').strip()
    dept_id = request.args.get('deptId', type=int)
    
    query = User.query.filter_by(del_flag='0')
    
    if login_name:
        query = query.filter(User.login_name.like(f'%{login_name}%'))
    if phonenumber:
        query = query.filter(User.phonenumber.like(f'%{phonenumber}%'))
    if status:
        query = query.filter_by(status=status)
    if dept_id:
        query = query.filter_by(dept_id=dept_id)
    
    users, total = paginate(query.order_by(User.create_time.desc()), page, per_page)
    
    # 转换为字典
    rows = []
    for user in users:
        row = {
            'user_id': user.user_id,
            'login_name': user.login_name,
            'user_name': user.user_name,
            'email': user.email,
            'phonenumber': user.phonenumber,
            'sex': user.sex,
            'status': user.status,
            'dept_name': user.dept.dept_name if user.dept else '',
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S') if user.create_time else ''
        }
        rows.append(row)
    
    return table_response(rows, total)


@system_bp.route('/role/list')
@login_required
@permission_required('system:role:view')
def role_list():
    """角色列表页面"""
    return render_template('system/role/role.html')


@system_bp.route('/menu/list')
@login_required
@permission_required('system:menu:view')
def menu_list():
    """菜单列表页面"""
    return render_template('system/menu/menu.html')


@system_bp.route('/dept/list')
@login_required
@permission_required('system:dept:view')
def dept_list():
    """部门列表页面"""
    return render_template('system/dept/dept.html')


@system_bp.route('/post/list')
@login_required
@permission_required('system:post:view')
def post_list():
    """岗位列表页面"""
    return render_template('system/post/post.html')


@system_bp.route('/dict/list')
@login_required
@permission_required('system:dict:view')
def dict_list():
    """字典列表页面"""
    return render_template('system/dict/type/type.html')


@system_bp.route('/config/list')
@login_required
@permission_required('system:config:view')
def config_list():
    """参数配置列表页面"""
    return render_template('system/config/config.html')


@system_bp.route('/notice/list')
@login_required
@permission_required('system:notice:view')
def notice_list():
    """通知公告列表页面"""
    return render_template('system/notice/notice.html')


# 用户管理API
@system_bp.route('/user/add', methods=['POST'])
@login_required
@permission_required('system:user:add')
def user_add():
    """添加用户"""
    try:
        data = request.form
        user = User(
            login_name=data.get('loginName'),
            user_name=data.get('userName'),
            dept_id=data.get('deptId', type=int),
            email=data.get('email'),
            phonenumber=data.get('phonenumber'),
            sex=data.get('sex', '0'),
            status=data.get('status', '0'),
            create_by=current_user.login_name,
            create_time=datetime.now()
        )
        user.set_password(data.get('password', '123456'))
        
        db.session.add(user)
        db.session.commit()
        
        return success_response('添加成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'添加失败: {str(e)}')


@system_bp.route('/user/edit', methods=['POST'])
@login_required
@permission_required('system:user:edit')
def user_edit():
    """编辑用户"""
    try:
        user_id = request.form.get('userId', type=int)
        user = User.query.get_or_404(user_id)
        
        user.user_name = request.form.get('userName')
        user.dept_id = request.form.get('deptId', type=int)
        user.email = request.form.get('email')
        user.phonenumber = request.form.get('phonenumber')
        user.sex = request.form.get('sex')
        user.status = request.form.get('status')
        user.update_by = current_user.login_name
        user.update_time = datetime.now()
        
        db.session.commit()
        
        return success_response('修改成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改失败: {str(e)}')


@system_bp.route('/user/remove', methods=['POST'])
@login_required
@permission_required('system:user:remove')
def user_remove():
    """删除用户"""
    try:
        user_ids = request.form.get('ids', '').split(',')
        for user_id in user_ids:
            if user_id:
                user = User.query.get(int(user_id))
                if user:
                    user.del_flag = '2'
        
        db.session.commit()
        return success_response('删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')


# 岗位管理API
@system_bp.route('/post/list/data')
@login_required
def post_list_data():
    """岗位列表数据"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    post_name = request.args.get('postName', '').strip()
    status = request.args.get('status', '').strip()
    
    query = Post.query
    if post_name:
        query = query.filter(Post.post_name.like(f'%{post_name}%'))
    if status:
        query = query.filter_by(status=status)
    
    posts, total = paginate(query.order_by(Post.post_sort), page, per_page)
    
    rows = []
    for post in posts:
        rows.append({
            'post_id': post.post_id,
            'post_code': post.post_code,
            'post_name': post.post_name,
            'post_sort': post.post_sort,
            'status': post.status,
            'create_time': post.create_time.strftime('%Y-%m-%d %H:%M:%S') if post.create_time else ''
        })
    
    return table_response(rows, total)


@system_bp.route('/post/add', methods=['POST'])
@login_required
def post_add():
    """新增岗位"""
    try:
        post = Post(
            post_code=request.form.get('postCode'),
            post_name=request.form.get('postName'),
            post_sort=request.form.get('postSort', 0, type=int),
            status=request.form.get('status', '0'),
            remark=request.form.get('remark', ''),
            create_by=current_user.login_name,
            create_time=datetime.now()
        )
        db.session.add(post)
        db.session.commit()
        return success_response('新增成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'新增失败: {str(e)}')


@system_bp.route('/post/edit', methods=['POST'])
@login_required
def post_edit():
    """编辑岗位"""
    try:
        post_id = request.form.get('postId', type=int)
        post = Post.query.get_or_404(post_id)
        
        post.post_code = request.form.get('postCode')
        post.post_name = request.form.get('postName')
        post.post_sort = request.form.get('postSort', type=int)
        post.status = request.form.get('status')
        post.remark = request.form.get('remark', '')
        post.update_by = current_user.login_name
        post.update_time = datetime.now()
        
        db.session.commit()
        return success_response('修改成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改失败: {str(e)}')


@system_bp.route('/post/remove', methods=['POST'])
@login_required
def post_remove():
    """删除岗位"""
    try:
        post_ids = request.form.get('ids', '').split(',')
        for post_id in post_ids:
            if post_id:
                Post.query.filter_by(post_id=int(post_id)).delete()
        db.session.commit()
        return success_response('删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')


# 部门管理API
@system_bp.route('/dept/tree')
@login_required
def dept_tree():
    """部门树形数据"""
    depts = Dept.query.order_by(Dept.parent_id, Dept.order_num).all()
    
    def build_tree(parent_id=0):
        result = []
        for dept in depts:
            if dept.parent_id == parent_id:
                node = {
                    'dept_id': dept.dept_id,
                    'dept_name': dept.dept_name,
                    'parent_id': dept.parent_id,
                    'order_num': dept.order_num,
                    'status': dept.status,
                    'create_time': dept.create_time.strftime('%Y-%m-%d %H:%M:%S') if dept.create_time else '',
                    'children': build_tree(dept.dept_id)
                }
                result.append(node)
        return result
    
    tree_data = build_tree(0)
    return success_response('查询成功', tree_data)


@system_bp.route('/dept/add', methods=['POST'])
@login_required
def dept_add():
    """新增部门"""
    try:
        dept = Dept(
            parent_id=request.form.get('parentId', 0, type=int),
            dept_name=request.form.get('deptName'),
            order_num=request.form.get('orderNum', 0, type=int),
            leader=request.form.get('leader', ''),
            phone=request.form.get('phone', ''),
            email=request.form.get('email', ''),
            status=request.form.get('status', '0'),
            create_by=current_user.login_name,
            create_time=datetime.now()
        )
        db.session.add(dept)
        db.session.commit()
        return success_response('新增成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'新增失败: {str(e)}')


@system_bp.route('/dept/edit', methods=['POST'])
@login_required
def dept_edit():
    """编辑部门"""
    try:
        dept_id = request.form.get('deptId', type=int)
        dept = Dept.query.get_or_404(dept_id)
        
        dept.parent_id = request.form.get('parentId', type=int)
        dept.dept_name = request.form.get('deptName')
        dept.order_num = request.form.get('orderNum', type=int)
        dept.leader = request.form.get('leader', '')
        dept.phone = request.form.get('phone', '')
        dept.email = request.form.get('email', '')
        dept.status = request.form.get('status')
        dept.update_by = current_user.login_name
        dept.update_time = datetime.now()
        
        db.session.commit()
        return success_response('修改成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改失败: {str(e)}')


@system_bp.route('/dept/remove/<int:dept_id>', methods=['POST'])
@login_required
def dept_remove(dept_id):
    """删除部门"""
    try:
        # 检查是否有子部门
        if Dept.query.filter_by(parent_id=dept_id).first():
            return error_response('存在子部门，不允许删除')
        
        # 检查是否有关联用户
        if User.query.filter_by(dept_id=dept_id).first():
            return error_response('部门下存在用户，不允许删除')
        
        Dept.query.filter_by(dept_id=dept_id).delete()
        db.session.commit()
        return success_response('删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')


# 角色管理API
@system_bp.route('/role/list/data')
@login_required
def role_list_data():
    """角色列表数据"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    role_name = request.args.get('roleName', '').strip()
    role_key = request.args.get('roleKey', '').strip()
    status = request.args.get('status', '').strip()
    
    query = Role.query.filter_by(del_flag='0')
    if role_name:
        query = query.filter(Role.role_name.like(f'%{role_name}%'))
    if role_key:
        query = query.filter(Role.role_key.like(f'%{role_key}%'))
    if status:
        query = query.filter_by(status=status)
    
    roles, total = paginate(query.order_by(Role.role_sort), page, per_page)
    
    rows = []
    for role in roles:
        rows.append({
            'role_id': role.role_id,
            'role_name': role.role_name,
            'role_key': role.role_key,
            'role_sort': role.role_sort,
            'status': role.status,
            'create_time': role.create_time.strftime('%Y-%m-%d %H:%M:%S') if role.create_time else ''
        })
    
    return table_response(rows, total)


@system_bp.route('/role/add', methods=['POST'])
@login_required
def role_add():
    """新增角色"""
    try:
        role = Role(
            role_name=request.form.get('roleName'),
            role_key=request.form.get('roleKey'),
            role_sort=request.form.get('roleSort', 0, type=int),
            status=request.form.get('status', '0'),
            remark=request.form.get('remark', ''),
            create_by=current_user.login_name,
            create_time=datetime.now()
        )
        db.session.add(role)
        db.session.commit()
        return success_response('新增成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'新增失败: {str(e)}')


@system_bp.route('/role/edit', methods=['POST'])
@login_required
def role_edit():
    """编辑角色"""
    try:
        role_id = request.form.get('roleId', type=int)
        role = Role.query.get_or_404(role_id)
        
        role.role_name = request.form.get('roleName')
        role.role_key = request.form.get('roleKey')
        role.role_sort = request.form.get('roleSort', type=int)
        role.status = request.form.get('status')
        role.remark = request.form.get('remark', '')
        role.update_by = current_user.login_name
        role.update_time = datetime.now()
        
        db.session.commit()
        return success_response('修改成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改失败: {str(e)}')


@system_bp.route('/role/remove', methods=['POST'])
@login_required
def role_remove():
    """删除角色"""
    try:
        role_ids = request.form.get('ids', '').split(',')
        for role_id in role_ids:
            if role_id:
                role = Role.query.get(int(role_id))
                if role:
                    role.del_flag = '2'
        db.session.commit()
        return success_response('删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')


# 菜单管理API
@system_bp.route('/menu/tree')
@login_required
def menu_tree():
    """菜单树形数据"""
    menus = Menu.query.order_by(Menu.parent_id, Menu.order_num).all()
    
    def build_tree(parent_id=0):
        result = []
        for menu in menus:
            if menu.parent_id == parent_id:
                node = {
                    'menu_id': menu.menu_id,
                    'menu_name': menu.menu_name,
                    'parent_id': menu.parent_id,
                    'order_num': menu.order_num,
                    'url': menu.url,
                    'menu_type': menu.menu_type,
                    'visible': menu.visible,
                    'status': menu.status,
                    'perms': menu.perms,
                    'icon': menu.icon,
                    'children': build_tree(menu.menu_id)
                }
                result.append(node)
        return result
    
    tree_data = build_tree(0)
    return success_response('查询成功', tree_data)


@system_bp.route('/menu/add', methods=['POST'])
@login_required
def menu_add():
    """新增菜单"""
    try:
        menu = Menu(
            parent_id=request.form.get('parentId', 0, type=int),
            menu_name=request.form.get('menuName'),
            menu_type=request.form.get('menuType', 'C'),
            order_num=request.form.get('orderNum', 0, type=int),
            url=request.form.get('url', ''),
            perms=request.form.get('perms', ''),
            icon=request.form.get('icon', ''),
            visible=request.form.get('visible', '0'),
            status=request.form.get('status', '0'),
            create_by=current_user.login_name,
            create_time=datetime.now()
        )
        db.session.add(menu)
        db.session.commit()
        return success_response('新增成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'新增失败: {str(e)}')


@system_bp.route('/menu/edit', methods=['POST'])
@login_required
def menu_edit():
    """编辑菜单"""
    try:
        menu_id = request.form.get('menuId', type=int)
        menu = Menu.query.get_or_404(menu_id)
        
        menu.parent_id = request.form.get('parentId', type=int)
        menu.menu_name = request.form.get('menuName')
        menu.menu_type = request.form.get('menuType')
        menu.order_num = request.form.get('orderNum', type=int)
        menu.url = request.form.get('url', '')
        menu.perms = request.form.get('perms', '')
        menu.icon = request.form.get('icon', '')
        menu.visible = request.form.get('visible')
        menu.status = request.form.get('status')
        menu.update_by = current_user.login_name
        menu.update_time = datetime.now()
        
        db.session.commit()
        return success_response('修改成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改失败: {str(e)}')


@system_bp.route('/menu/remove/<int:menu_id>', methods=['POST'])
@login_required
def menu_remove(menu_id):
    """删除菜单"""
    try:
        # 检查是否有子菜单
        if Menu.query.filter_by(parent_id=menu_id).first():
            return error_response('存在子菜单，不允许删除')
        
        Menu.query.filter_by(menu_id=menu_id).delete()
        db.session.commit()
        return success_response('删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')
