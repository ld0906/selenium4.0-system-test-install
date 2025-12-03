"""
数据库初始化脚本
创建数据库表并插入初始数据
"""
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.models import (
    db, User, Role, Menu, Dept, Post, DictType, DictData,
    Config, user_role, role_menu
)

def init_database():
    """初始化数据库"""
    app = create_app('default')
    
    with app.app_context():
        print('开始初始化数据库...')
        
        # 删除所有表
        db.drop_all()
        print('已删除旧表')
        
        # 创建所有表
        db.create_all()
        print('已创建数据库表')
        
        # 插入初始数据
        insert_initial_data()
        
        print('数据库初始化完成！')
        print('')
        print('=' * 50)
        print('默认管理员账号:')
        print('用户名: admin')
        print('密码: admin123')
        print('=' * 50)


def insert_initial_data():
    """插入初始数据"""
    
    # 1. 创建部门
    print('插入部门数据...')
    dept_root = Dept(
        dept_id=100,
        parent_id=0,
        ancestors='0',
        dept_name='大牛科技',
        order_num=0,
        leader='admin',
        status='0',
        create_time=datetime.now()
    )
    
    dept_tech = Dept(
        dept_id=101,
        parent_id=100,
        ancestors='0,100',
        dept_name='技术部',
        order_num=1,
        leader='admin',
        status='0',
        create_time=datetime.now()
    )
    
    dept_market = Dept(
        dept_id=102,
        parent_id=100,
        ancestors='0,100',
        dept_name='市场部',
        order_num=2,
        status='0',
        create_time=datetime.now()
    )
    
    db.session.add_all([dept_root, dept_tech, dept_market])
    
    # 2. 创建岗位
    print('插入岗位数据...')
    post1 = Post(
        post_id=1,
        post_code='ceo',
        post_name='董事长',
        post_sort=1,
        status='0',
        create_time=datetime.now()
    )
    
    post2 = Post(
        post_id=2,
        post_code='se',
        post_name='项目经理',
        post_sort=2,
        status='0',
        create_time=datetime.now()
    )
    
    post3 = Post(
        post_id=3,
        post_code='hr',
        post_name='人力资源',
        post_sort=3,
        status='0',
        create_time=datetime.now()
    )
    
    post4 = Post(
        post_id=4,
        post_code='user',
        post_name='普通员工',
        post_sort=4,
        status='0',
        create_time=datetime.now()
    )
    
    db.session.add_all([post1, post2, post3, post4])
    
    # 3. 创建角色
    print('插入角色数据...')
    role_admin = Role(
        role_id=1,
        role_name='超级管理员',
        role_key='admin',
        role_sort=1,
        data_scope='1',
        status='0',
        create_time=datetime.now(),
        remark='超级管理员'
    )
    
    role_common = Role(
        role_id=2,
        role_name='普通角色',
        role_key='common',
        role_sort=2,
        data_scope='2',
        status='0',
        create_time=datetime.now(),
        remark='普通角色'
    )
    
    db.session.add_all([role_admin, role_common])
    
    # 4. 创建菜单
    print('插入菜单数据...')
    menus = []
    
    # 系统管理
    menu_system = Menu(
        menu_id=1,
        menu_name='系统管理',
        parent_id=0,
        order_num=1,
        url='#',
        menu_type='M',
        visible='0',
        perms='',
        icon='fa fa-gear',
        create_time=datetime.now()
    )
    menus.append(menu_system)
    
    # 用户管理
    menu_user = Menu(
        menu_id=100,
        menu_name='用户管理',
        parent_id=1,
        order_num=1,
        url='/system/user/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:user:view',
        icon='fa fa-user-o',
        create_time=datetime.now()
    )
    menus.append(menu_user)
    
    # 角色管理
    menu_role = Menu(
        menu_id=101,
        menu_name='角色管理',
        parent_id=1,
        order_num=2,
        url='/system/role/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:role:view',
        icon='fa fa-user-secret',
        create_time=datetime.now()
    )
    menus.append(menu_role)
    
    # 菜单管理
    menu_menu = Menu(
        menu_id=102,
        menu_name='菜单管理',
        parent_id=1,
        order_num=3,
        url='/system/menu/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:menu:view',
        icon='fa fa-th-list',
        create_time=datetime.now()
    )
    menus.append(menu_menu)
    
    # 部门管理
    menu_dept = Menu(
        menu_id=103,
        menu_name='部门管理',
        parent_id=1,
        order_num=4,
        url='/system/dept/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:dept:view',
        icon='fa fa-outdent',
        create_time=datetime.now()
    )
    menus.append(menu_dept)
    
    # 岗位管理
    menu_post = Menu(
        menu_id=104,
        menu_name='岗位管理',
        parent_id=1,
        order_num=5,
        url='/system/post/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:post:view',
        icon='fa fa-address-card-o',
        create_time=datetime.now()
    )
    menus.append(menu_post)
    
    # 字典管理
    menu_dict = Menu(
        menu_id=105,
        menu_name='字典管理',
        parent_id=1,
        order_num=6,
        url='/system/dict/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:dict:view',
        icon='fa fa-bookmark-o',
        create_time=datetime.now()
    )
    menus.append(menu_dict)
    
    # 参数设置
    menu_config = Menu(
        menu_id=106,
        menu_name='参数设置',
        parent_id=1,
        order_num=7,
        url='/system/config/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:config:view',
        icon='fa fa-sun-o',
        create_time=datetime.now()
    )
    menus.append(menu_config)
    
    # 通知公告
    menu_notice = Menu(
        menu_id=107,
        menu_name='通知公告',
        parent_id=1,
        order_num=8,
        url='/system/notice/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='system:notice:view',
        icon='fa fa-bullhorn',
        create_time=datetime.now()
    )
    menus.append(menu_notice)
    
    # 系统监控
    menu_monitor = Menu(
        menu_id=2,
        menu_name='系统监控',
        parent_id=0,
        order_num=2,
        url='#',
        menu_type='M',
        visible='0',
        perms='',
        icon='fa fa-video-camera',
        create_time=datetime.now()
    )
    menus.append(menu_monitor)
    
    # 在线用户
    menu_online = Menu(
        menu_id=108,
        menu_name='在线用户',
        parent_id=2,
        order_num=1,
        url='/monitor/online/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='monitor:online:view',
        icon='fa fa-user-circle',
        create_time=datetime.now()
    )
    menus.append(menu_online)
    
    # 定时任务
    menu_job = Menu(
        menu_id=109,
        menu_name='定时任务',
        parent_id=2,
        order_num=2,
        url='/monitor/job/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='monitor:job:view',
        icon='fa fa-tasks',
        create_time=datetime.now()
    )
    menus.append(menu_job)
    
    # 操作日志
    menu_operlog = Menu(
        menu_id=110,
        menu_name='操作日志',
        parent_id=2,
        order_num=3,
        url='/monitor/operlog/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='monitor:operlog:view',
        icon='fa fa-address-book',
        create_time=datetime.now()
    )
    menus.append(menu_operlog)
    
    # 登录日志
    menu_logininfor = Menu(
        menu_id=111,
        menu_name='登录日志',
        parent_id=2,
        order_num=4,
        url='/monitor/logininfor/list',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='monitor:logininfor:view',
        icon='fa fa-info-circle',
        create_time=datetime.now()
    )
    menus.append(menu_logininfor)
    
    # 服务监控
    menu_server = Menu(
        menu_id=112,
        menu_name='服务监控',
        parent_id=2,
        order_num=5,
        url='/monitor/server',
        target='menuItem',
        menu_type='C',
        visible='0',
        perms='monitor:server:view',
        icon='fa fa-server',
        create_time=datetime.now()
    )
    menus.append(menu_server)
    
    db.session.add_all(menus)
    
    # 5. 创建管理员用户
    print('插入用户数据...')
    admin_user = User(
        user_id=1,
        dept_id=100,
        login_name='admin',
        user_name='管理员',
        user_type='00',
        email='admin@dntest.com',
        phonenumber='15888888888',
        sex='0',
        status='0',
        create_time=datetime.now()
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # 提交以获取ID
    db.session.commit()
    
    # 6. 关联用户和角色
    print('关联用户角色...')
    db.session.execute(
        user_role.insert().values(user_id=1, role_id=1)
    )
    
    # 7. 关联角色和菜单(管理员拥有所有菜单)
    print('关联角色菜单...')
    for menu in menus:
        db.session.execute(
            role_menu.insert().values(role_id=1, menu_id=menu.menu_id)
        )
    
    # 8. 插入字典类型和数据
    print('插入字典数据...')
    dict_type_sex = DictType(
        dict_name='用户性别',
        dict_type='sys_user_sex',
        status='0',
        create_time=datetime.now()
    )
    db.session.add(dict_type_sex)
    
    dict_data_sex = [
        DictData(dict_sort=1, dict_label='男', dict_value='0', dict_type='sys_user_sex', css_class='', list_class='', is_default='Y', status='0', create_time=datetime.now()),
        DictData(dict_sort=2, dict_label='女', dict_value='1', dict_type='sys_user_sex', css_class='', list_class='', is_default='N', status='0', create_time=datetime.now()),
        DictData(dict_sort=3, dict_label='未知', dict_value='2', dict_type='sys_user_sex', css_class='', list_class='', is_default='N', status='0', create_time=datetime.now())
    ]
    db.session.add_all(dict_data_sex)
    
    dict_type_status = DictType(
        dict_name='系统状态',
        dict_type='sys_normal_disable',
        status='0',
        create_time=datetime.now()
    )
    db.session.add(dict_type_status)
    
    dict_data_status = [
        DictData(dict_sort=1, dict_label='正常', dict_value='0', dict_type='sys_normal_disable', css_class='primary', list_class='primary', is_default='Y', status='0', create_time=datetime.now()),
        DictData(dict_sort=2, dict_label='停用', dict_value='1', dict_type='sys_normal_disable', css_class='danger', list_class='danger', is_default='N', status='0', create_time=datetime.now())
    ]
    db.session.add_all(dict_data_status)
    
    # 9. 插入系统配置
    print('插入系统配置...')
    config1 = Config(
        config_name='系统名称',
        config_key='sys.name',
        config_value='大牛测试系统',
        config_type='Y',
        create_time=datetime.now()
    )
    
    config2 = Config(
        config_name='用户初始密码',
        config_key='sys.user.initPassword',
        config_value='123456',
        config_type='Y',
        create_time=datetime.now()
    )
    
    db.session.add_all([config1, config2])
    
    # 提交所有更改
    db.session.commit()
    print('初始数据插入完成')


if __name__ == '__main__':
    init_database()
