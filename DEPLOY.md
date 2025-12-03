# 大牛测试系统 - 部署指南

## 📋 目录

1. [系统要求](#系统要求)
2. [快速部署](#快速部署)
3. [详细步骤](#详细步骤)
4. [静态资源配置](#静态资源配置)
5. [生产环境部署](#生产环境部署)
6. [常见问题](#常见问题)

## 系统要求

- Python 3.8 或更高版本
- pip (Python包管理器)
- 2GB以上可用内存
- Windows/Linux/Mac操作系统

## 快速部署

### Windows 用户

1. 双击运行 `start.bat`
2. 等待依赖安装和数据库初始化
3. 浏览器访问 http://localhost:5000
4. 使用 admin / admin123 登录

### Linux/Mac 用户

```bash
chmod +x start.sh
./start.sh
```

## 详细步骤

### 1. 安装Python依赖

```bash
# 创建虚拟环境(推荐)
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

如果下载速度慢,可以使用国内镜像:

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 初始化数据库

```bash
python init_db.py
```

这将创建SQLite数据库并插入初始数据,包括:
- 默认管理员账号: admin / admin123
- 基础角色和权限
- 系统菜单结构
- 演示字典数据

### 3. 启动应用

**开发环境:**

```bash
python run.py
```

**生产环境:**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 4. 访问系统

打开浏览器访问: http://localhost:5000

默认账号:
- 用户名: admin
- 密码: admin123

## 静态资源配置

### 方式一: 使用CDN(推荐)

修改模板文件中的静态资源链接为CDN:

```html
<!-- Bootstrap CSS -->
<link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">

<!-- Font Awesome -->
<link href="https://cdn.bootcdn.net/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">

<!-- jQuery -->
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<!-- Bootstrap JS -->
<script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
```

### 方式二: 本地静态文件

1. 从原Java系统的`BOOT-INF/classes/static/`目录复制以下文件到`app/static/`:

```
app/static/
├── css/
│   ├── bootstrap.min.css
│   ├── font-awesome.min.css
│   ├── animate.min.css
│   ├── style.min.css
│   └── login.min.css
├── js/
│   ├── jquery.min.js
│   ├── bootstrap.min.js
│   └── plugins/
└── fonts/
    └── (Font Awesome 字体文件)
```

2. 或者下载开源库:

```bash
# Bootstrap
wget https://github.com/twbs/bootstrap/releases/download/v3.3.7/bootstrap-3.3.7-dist.zip

# jQuery
wget https://code.jquery.com/jquery-3.6.0.min.js

# Font Awesome
wget https://github.com/FortAwesome/Font-Awesome/releases/download/4.7.0/fontawesome-free-4.7.0-web.zip
```

## 生产环境部署

### 使用Gunicorn

1. 安装Gunicorn:

```bash
pip install gunicorn
```

2. 创建配置文件 `gunicorn_config.py`:

```python
bind = '0.0.0.0:5000'
workers = 4
worker_class = 'sync'
timeout = 60
keepalive = 5
errorlog = 'logs/gunicorn_error.log'
accesslog = 'logs/gunicorn_access.log'
loglevel = 'info'
```

3. 启动应用:

```bash
gunicorn -c gunicorn_config.py run:app
```

### 使用Nginx反向代理

1. 安装Nginx

2. 配置文件 `/etc/nginx/sites-available/dntest`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/dntest-python/app/static;
        expires 30d;
    }
}
```

3. 启用配置:

```bash
sudo ln -s /etc/nginx/sites-available/dntest /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 使用Systemd管理服务

创建文件 `/etc/systemd/system/dntest.service`:

```ini
[Unit]
Description=DNTest Python Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/dntest-python
Environment="PATH=/path/to/dntest-python/venv/bin"
ExecStart=/path/to/dntest-python/venv/bin/gunicorn -c gunicorn_config.py run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:

```bash
sudo systemctl daemon-reload
sudo systemctl start dntest
sudo systemctl enable dntest
sudo systemctl status dntest
```

### Docker部署

1. 创建 `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN python init_db.py

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

2. 构建和运行:

```bash
docker build -t dntest-python .
docker run -d -p 5000:5000 --name dntest dntest-python
```

## 常见问题

### Q1: 启动时提示"ModuleNotFoundError"

**A:** 确保已安装所有依赖:

```bash
pip install -r requirements.txt
```

### Q2: 数据库文件权限错误

**A:** 确保database目录有写权限:

```bash
chmod 755 database/
```

### Q3: 静态资源404错误

**A:** 可以使用CDN或从原系统复制静态文件,参考[静态资源配置](#静态资源配置)

### Q4: 验证码不显示

**A:** 确保安装了Pillow库:

```bash
pip install Pillow
```

### Q5: 如何修改默认端口

**A:** 编辑`run.py`,修改port参数:

```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Q6: 如何修改管理员密码

**A:** 运行以下Python代码:

```python
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    user = User.query.filter_by(login_name='admin').first()
    user.set_password('new_password')
    db.session.commit()
```

### Q7: 如何备份数据

**A:** 直接备份SQLite数据库文件:

```bash
cp database/dntest.db database/dntest_backup_$(date +%Y%m%d).db
```

### Q8: 如何迁移到MySQL/PostgreSQL

**A:** 修改`config.py`中的数据库URI:

```python
# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dbname'

# PostgreSQL  
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
```

## 安全建议

1. **修改SECRET_KEY**: 在`config.py`中设置强随机密钥
2. **修改默认密码**: 首次登录后立即修改admin密码
3. **禁用DEBUG模式**: 生产环境设置`DEBUG = False`
4. **配置HTTPS**: 使用SSL证书加密传输
5. **定期备份数据**: 设置定时任务备份数据库
6. **更新依赖**: 定期更新Python依赖包

## 性能优化

1. **使用缓存**: 配置Redis缓存会话和数据
2. **数据库索引**: 为常查询字段添加索引
3. **静态资源CDN**: 使用CDN加速静态资源
4. **Gunicorn工作进程**: 根据CPU核心数调整worker数量
5. **数据库连接池**: 配置合适的连接池大小

## 监控和日志

日志文件位置:
- 应用日志: `logs/dntest.log`
- Gunicorn错误日志: `logs/gunicorn_error.log`
- Gunicorn访问日志: `logs/gunicorn_access.log`

查看实时日志:

```bash
tail -f logs/dntest.log
```

## 技术支持

如遇到问题:
1. 查看日志文件
2. 检查配置是否正确
3. 确认Python版本和依赖版本
4. 参考README.md文档

---

祝您使用愉快！
