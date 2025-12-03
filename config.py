"""
应用配置文件
"""
import os
from datetime import timedelta

# 基础路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """配置基类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dntest-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "database", "dntest.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 生产环境设为False
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # 会话超时时间
    SESSION_COOKIE_NAME = 'dntest_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 分页配置
    PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # 上传配置
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 最大上传10MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # 日志配置
    LOG_FOLDER = os.path.join(BASE_DIR, 'logs')
    LOG_LEVEL = 'INFO'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 10
    
    # 验证码配置
    CAPTCHA_ENABLED = True
    CAPTCHA_LENGTH = 4
    CAPTCHA_EXPIRE = 300  # 5分钟过期
    
    # 记住我配置
    REMEMBER_ME_ENABLED = True
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # 密码策略
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_RETRY = 5  # 密码错误5次锁定账号
    PASSWORD_LOCK_TIME = 10  # 锁定10分钟
    
    # 系统配置
    SYSTEM_NAME = '大牛测试系统'
    SYSTEM_VERSION = '1.0.0'
    COPYRIGHT = 'Copyright © 2025 Dntest All Rights Reserved.'
    DEMO_ENABLED = True  # 是否启用演示功能
    REGISTER_ENABLED = False  # 是否允许注册


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
