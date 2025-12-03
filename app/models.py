"""
数据库模型定义
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# 用户角色关联表
user_role = db.Table('sys_user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('sys_user.user_id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True)
)

# 角色菜单关联表
role_menu = db.Table('sys_role_menu',
    db.Column('role_id', db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('sys_menu.menu_id'), primary_key=True)
)

# 角色部门关联表
role_dept = db.Table('sys_role_dept',
    db.Column('role_id', db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True),
    db.Column('dept_id', db.Integer, db.ForeignKey('sys_dept.dept_id'), primary_key=True)
)

# 用户岗位关联表
user_post = db.Table('sys_user_post',
    db.Column('user_id', db.Integer, db.ForeignKey('sys_user.user_id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('sys_post.post_id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """用户表"""
    __tablename__ = 'sys_user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('sys_dept.dept_id'))
    login_name = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_name = db.Column(db.String(30), nullable=False)
    user_type = db.Column(db.String(2), default='00')  # 00系统用户
    email = db.Column(db.String(50))
    phonenumber = db.Column(db.String(11))
    sex = db.Column(db.String(1), default='0')  # 0男 1女 2未知
    avatar = db.Column(db.String(100), default='')
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(20))  # 密码盐值(可选)
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    del_flag = db.Column(db.String(1), default='0')  # 0存在 2删除
    login_ip = db.Column(db.String(50))
    login_date = db.Column(db.DateTime)
    pwd_update_date = db.Column(db.DateTime)
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))
    
    # 关系
    dept = db.relationship('Dept', backref='users', lazy='joined')
    roles = db.relationship('Role', secondary=user_role, backref='users', lazy='dynamic')
    posts = db.relationship('Post', secondary=user_post, backref='users', lazy='dynamic')
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.pwd_update_date = datetime.now()
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        """是否是管理员"""
        return any(role.role_key == 'admin' for role in self.roles)
    
    def has_permission(self, permission):
        """检查是否有指定权限"""
        if self.is_admin():
            return True
        for role in self.roles:
            if role.status == '0':  # 角色正常状态
                for menu in role.menus:
                    if menu.perms and permission in menu.perms:
                        return True
        return False


class Role(db.Model):
    """角色表"""
    __tablename__ = 'sys_role'
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(30), nullable=False)
    role_key = db.Column(db.String(100), unique=True, nullable=False)
    role_sort = db.Column(db.Integer, default=0)
    data_scope = db.Column(db.String(1), default='1')  # 数据范围：1全部 2自定义 3本部门 4本部门及以下 5仅本人
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    del_flag = db.Column(db.String(1), default='0')  # 0存在 2删除
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))
    
    # 关系
    menus = db.relationship('Menu', secondary=role_menu, backref='roles', lazy='dynamic')
    depts = db.relationship('Dept', secondary=role_dept, backref='roles', lazy='dynamic')


class Menu(db.Model):
    """菜单表"""
    __tablename__ = 'sys_menu'
    
    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, default=0)  # 父菜单ID
    order_num = db.Column(db.Integer, default=0)
    url = db.Column(db.String(200), default='#')
    target = db.Column(db.String(20), default='')  # 打开方式：menuItem页签 menuBlank新窗口
    menu_type = db.Column(db.String(1), default='M')  # M目录 C菜单 F按钮
    visible = db.Column(db.String(1), default='0')  # 0显示 1隐藏
    is_refresh = db.Column(db.String(1), default='1')  # 0刷新 1不刷新
    perms = db.Column(db.String(100))  # 权限标识
    icon = db.Column(db.String(100), default='#')
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class Dept(db.Model):
    """部门表"""
    __tablename__ = 'sys_dept'
    
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, default=0)
    ancestors = db.Column(db.String(50), default='')  # 祖级列表
    dept_name = db.Column(db.String(30), nullable=False)
    order_num = db.Column(db.Integer, default=0)
    leader = db.Column(db.String(20))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(50))
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    del_flag = db.Column(db.String(1), default='0')  # 0存在 2删除
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)


class Post(db.Model):
    """岗位表"""
    __tablename__ = 'sys_post'
    
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_code = db.Column(db.String(64), unique=True, nullable=False)
    post_name = db.Column(db.String(50), nullable=False)
    post_sort = db.Column(db.Integer, default=0)
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class DictType(db.Model):
    """字典类型表"""
    __tablename__ = 'sys_dict_type'
    
    dict_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dict_name = db.Column(db.String(100), nullable=False)
    dict_type = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class DictData(db.Model):
    """字典数据表"""
    __tablename__ = 'sys_dict_data'
    
    dict_code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dict_sort = db.Column(db.Integer, default=0)
    dict_label = db.Column(db.String(100), nullable=False)
    dict_value = db.Column(db.String(100), nullable=False)
    dict_type = db.Column(db.String(100), nullable=False)
    css_class = db.Column(db.String(100))
    list_class = db.Column(db.String(100))  # 表格回显样式
    is_default = db.Column(db.String(1), default='N')  # Y是 N否
    status = db.Column(db.String(1), default='0')  # 0正常 1停用
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class Config(db.Model):
    """参数配置表"""
    __tablename__ = 'sys_config'
    
    config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_name = db.Column(db.String(100), nullable=False)
    config_key = db.Column(db.String(100), unique=True, nullable=False)
    config_value = db.Column(db.String(500), nullable=False)
    config_type = db.Column(db.String(1), default='N')  # Y系统内置 N非系统内置
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class Notice(db.Model):
    """通知公告表"""
    __tablename__ = 'sys_notice'
    
    notice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notice_title = db.Column(db.String(50), nullable=False)
    notice_type = db.Column(db.String(1), nullable=False)  # 1通知 2公告
    notice_content = db.Column(db.Text)
    status = db.Column(db.String(1), default='0')  # 0正常 1关闭
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class OperLog(db.Model):
    """操作日志表"""
    __tablename__ = 'sys_oper_log'
    
    oper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))  # 模块标题
    business_type = db.Column(db.Integer, default=0)  # 业务类型：0其它 1新增 2修改 3删除
    method = db.Column(db.String(100))  # 方法名称
    request_method = db.Column(db.String(10))  # 请求方式
    operator_type = db.Column(db.Integer, default=0)  # 操作类别：0其它 1后台用户 2手机端用户
    oper_name = db.Column(db.String(50))  # 操作人员
    dept_name = db.Column(db.String(50))  # 部门名称
    oper_url = db.Column(db.String(255))  # 请求URL
    oper_ip = db.Column(db.String(50))  # 主机地址
    oper_location = db.Column(db.String(255))  # 操作地点
    oper_param = db.Column(db.Text)  # 请求参数
    json_result = db.Column(db.Text)  # 返回参数
    status = db.Column(db.Integer, default=0)  # 操作状态：0正常 1异常
    error_msg = db.Column(db.Text)  # 错误消息
    oper_time = db.Column(db.DateTime, default=datetime.now)


class LoginInfo(db.Model):
    """登录日志表"""
    __tablename__ = 'sys_logininfor'
    
    info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_name = db.Column(db.String(50))  # 登录账号
    ipaddr = db.Column(db.String(50))  # 登录IP地址
    login_location = db.Column(db.String(255))  # 登录地点
    browser = db.Column(db.String(50))  # 浏览器类型
    os = db.Column(db.String(50))  # 操作系统
    status = db.Column(db.String(1), default='0')  # 登录状态：0成功 1失败
    msg = db.Column(db.String(255))  # 提示消息
    login_time = db.Column(db.DateTime, default=datetime.now)


class OnlineUser(db.Model):
    """在线用户表"""
    __tablename__ = 'sys_user_online'
    
    sessionId = db.Column(db.String(50), primary_key=True)
    login_name = db.Column(db.String(50))
    dept_name = db.Column(db.String(50))
    ipaddr = db.Column(db.String(50))
    login_location = db.Column(db.String(255))
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    status = db.Column(db.String(10))  # on_line在线 off_line离线
    start_timestamp = db.Column(db.DateTime)
    last_access_time = db.Column(db.DateTime)
    expire_time = db.Column(db.Integer)  # 超时时间(分钟)


class Job(db.Model):
    """定时任务表"""
    __tablename__ = 'sys_job'
    
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(64), nullable=False)
    job_group = db.Column(db.String(64), nullable=False)
    invoke_target = db.Column(db.String(500), nullable=False)  # 调用目标字符串
    cron_expression = db.Column(db.String(255))  # cron执行表达式
    misfire_policy = db.Column(db.String(20), default='3')  # 计划执行错误策略：1立即执行 2执行一次 3放弃执行
    concurrent = db.Column(db.String(1), default='1')  # 是否并发执行：0允许 1禁止
    status = db.Column(db.String(1), default='0')  # 状态：0正常 1暂停
    create_by = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_by = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(500))


class JobLog(db.Model):
    """定时任务日志表"""
    __tablename__ = 'sys_job_log'
    
    job_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(64), nullable=False)
    job_group = db.Column(db.String(64), nullable=False)
    invoke_target = db.Column(db.String(500), nullable=False)
    job_message = db.Column(db.String(500))
    status = db.Column(db.String(1), default='0')  # 执行状态：0正常 1失败
    exception_info = db.Column(db.Text)  # 异常信息
    create_time = db.Column(db.DateTime, default=datetime.now)
