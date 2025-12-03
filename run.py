"""
应用启动文件
"""
import os
from app import create_app

# 从环境变量获取配置，默认为development
config_name = os.environ.get('FLASK_CONFIG', 'development')

# 创建应用实例
app = create_app(config_name)

if __name__ == '__main__':
    # 开发环境启动配置
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
