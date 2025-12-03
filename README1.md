# 大牛测试系统 - Python版

基于Python Flask框架重新实现的管理系统，保持与原系统相同的UI和功能。

## 技术栈

- **后端**: Flask 3.0
- **数据库**: SQLite3
- **模板引擎**: Jinja2
- **前端**: Bootstrap 3.3.7 + jQuery + AdminLTE风格
- **权限认证**: Flask-Login + 自定义权限装饰器

## 功能模块

### 系统管理
- 用户管理：用户的增删改查、密码重置、角色分配
- 角色管理：角色权限配置、数据权限设置
- 菜单管理：菜单的增删改查、权限标识配置
- 部门管理：部门树形结构管理
- 岗位管理：岗位信息维护
- 字典管理：系统字典数据维护
- 参数配置：系统参数配置

### 系统监控
- 在线用户：查看当前在线用户
- 定时任务：定时任务配置和执行
- 数据监控：数据库连接池监控
- 服务监控：服务器性能监控
- 操作日志：系统操作日志记录
- 登录日志：用户登录日志记录

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

这将创建SQLite数据库并初始化基础数据，包括：
- 管理员账号：admin / admin123
- 基础角色和权限
- 系统菜单结构
- 演示数据

### 3. 启动应用

```bash
python run.py
```

或者使用启动脚本：

**Windows**:
```bash
start.bat
```

**Linux/Mac**:
```bash
chmod +x start.sh
./start.sh
```

### 4. 访问系统

打开浏览器访问: http://localhost:5000

默认账号：
- 用户名：admin
- 密码：admin123

## 项目结构

```
dntest-python/
├── app/                      # 应用主目录
│   ├── __init__.py          # Flask应用初始化
│   ├── models.py            # 数据模型
│   ├── auth.py              # 认证相关
│   ├── decorators.py        # 权限装饰器
│   ├── utils.py             # 工具函数
│   ├── routes/              # 路由模块
│   │   ├── __init__.py
│   │   ├── main.py          # 主页路由
│   │   ├── auth.py          # 登录注册路由
│   │   ├── system.py        # 系统管理路由
│   │   └── monitor.py       # 系统监控路由
│   ├── templates/           # HTML模板
│   │   ├── base.html        # 基础模板
│   │   ├── login.html       # 登录页面
│   │   ├── index.html       # 首页框架
│   │   ├── system/          # 系统管理模板
│   │   └── monitor/         # 系统监控模板
│   └── static/              # 静态资源
│       ├── css/             # 样式文件
│       ├── js/              # JavaScript文件
│       ├── img/             # 图片资源
│       └── plugins/         # 第三方插件
├── database/                # 数据库文件目录
│   └── dntest.db           # SQLite数据库
├── logs/                    # 日志目录
├── config.py                # 配置文件
├── init_db.py              # 数据库初始化脚本
├── run.py                  # 启动文件
├── requirements.txt        # Python依赖
├── start.bat               # Windows启动脚本
├── start.sh                # Linux启动脚本
└── README.md               # 说明文档
```

## 配置说明

编辑 `config.py` 文件进行配置：

```python
# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/dntest.db'

# 会话密钥
SECRET_KEY = 'your-secret-key-here'

# 分页配置
PAGE_SIZE = 10

# 日志配置
LOG_LEVEL = 'INFO'
```

## 开发说明

### 添加新功能模块

1. 在 `app/models.py` 中定义数据模型
2. 在 `app/routes/` 中创建对应的路由文件
3. 在 `app/templates/` 中创建对应的HTML模板
4. 在 `app/__init__.py` 中注册新的蓝图

### 权限控制

使用装饰器控制访问权限：

```python
from app.decorators import login_required, permission_required

@bp.route('/admin')
@login_required
@permission_required('system:user:list')
def admin_page():
    return render_template('admin.html')
```


## 许可证

本项目仅供学习和测试使用。

## 联系方式

如有问题，请提交Issue。
