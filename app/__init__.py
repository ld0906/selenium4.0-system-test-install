"""
Flask应用初始化
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_login import LoginManager
from config import config
from app.models import db, User

login_manager = LoginManager()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 确保必要的目录存在
    ensure_directories(app)
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理
    register_error_handlers(app)
    
    # 配置日志
    configure_logging(app)
    
    # 注册模板过滤器和全局变量
    register_template_utils(app)
    
    return app


def ensure_directories(app):
    """确保必要的目录存在"""
    dirs = [
        app.config['UPLOAD_FOLDER'],
        app.config['LOG_FOLDER'],
        os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def init_extensions(app):
    """初始化Flask扩展"""
    # 初始化数据库
    db.init_app(app)
    
    # 初始化登录管理器
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录系统'
    login_manager.session_protection = 'strong'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app):
    """注册蓝图"""
    from app.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.system import system_bp
    from app.routes.monitor import monitor_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(system_bp, url_prefix='/system')
    app.register_blueprint(monitor_bp, url_prefix='/monitor')


def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500


def configure_logging(app):
    """配置日志"""
    if not app.debug:
        # 确保日志目录存在
        if not os.path.exists(app.config['LOG_FOLDER']):
            os.makedirs(app.config['LOG_FOLDER'])
        
        # 配置文件处理器
        file_handler = RotatingFileHandler(
            os.path.join(app.config['LOG_FOLDER'], 'dntest.log'),
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('DNTest startup')


def register_template_utils(app):
    """注册模板工具函数和全局变量"""
    from app.utils import get_dict_label, format_datetime, has_permission
    
    @app.context_processor
    def inject_global_vars():
        """注入全局变量"""
        return {
            'system_name': app.config['SYSTEM_NAME'],
            'system_version': app.config['SYSTEM_VERSION'],
            'copyright': app.config['COPYRIGHT'],
            'demo_enabled': app.config['DEMO_ENABLED']
        }
    
    @app.template_filter('dict_label')
    def dict_label_filter(dict_type, dict_value):
        """字典标签过滤器"""
        return get_dict_label(dict_type, dict_value)
    
    @app.template_filter('datetime')
    def datetime_filter(value, format='%Y-%m-%d %H:%M:%S'):
        """日期时间格式化过滤器"""
        return format_datetime(value, format)
    
    @app.template_test('permission')
    def permission_test(permission_str):
        """权限测试"""
        return has_permission(permission_str)
