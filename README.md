## 说明（重要！！！）： 这是新的被测系统，功能和老的系统几乎一致，但是有些元素的定位方式和书中提到的可能不太一致，需要读者根据书中讲诉的元素定位方法重新定位，刚好起到一个练习的作用。


### 步骤1: 进入项目目录
```bash
cd c:\Users\xxx\Documents\dntest-python
```

### 步骤2: 运行启动脚本

#### Windows用户:
双击 `start.bat` 或在命令行运行:
```bash
start.bat

```

#### Linux/Mac用户:
```bash
chmod +x start.sh
./start.sh
```

### 步骤3: 访问系统
打开浏览器访问: **http://localhost:5000**

### 步骤4: 登录
- 用户名: **admin**
- 密码: **admin123**

## 📌 首次使用说明

### 1. 脚本会自动完成以下操作:

✅ 检查Python环境  
✅ 创建虚拟环境(venv)  
✅ 安装所有依赖包  
✅ 初始化SQLite数据库  
✅ 创建管理员账号  
✅ 插入初始数据  
✅ 启动Web服务器  

### 2. 系统功能导航

登录后可以访问:

**左侧菜单:**
- 🏠 **首页**: 查看系统信息和用户信息
- 🔧 **系统管理**: 
  - 用户管理
  - 角色管理
  - 菜单管理
  - 部门管理
  - 岗位管理
  - 字典管理
  - 参数设置
  - 通知公告
- 📊 **系统监控**:
  - 在线用户
  - 定时任务
  - 操作日志
  - 登录日志
  - 服务监控

## 🛠️ 常用操作

### 查看用户列表
1. 点击 "系统管理" → "用户管理"
2. 可以搜索、新增、编辑、删除用户

### 修改个人密码
1. 点击顶部用户名
2. 选择"个人设置"
3. 修改密码

### 查看系统监控
1. 点击 "系统监控" → "服务监控"
2. 查看CPU、内存、磁盘使用情况

### 查看日志
1. 点击 "系统监控" → "操作日志" 或 "登录日志"
2. 可以按时间、用户名等条件筛选

## ⚙️ 手动安装(可选)

如果自动脚本失败，可以手动执行以下命令:

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_db.py

# 5. 启动应用
python run.py
```

## 🔍 故障排查

### 问题1: 提示"Python未安装"
**解决**: 下载安装Python 3.8+  
下载地址: https://www.python.org/downloads/

### 问题2: 依赖安装失败
**解决**: 使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: 端口5000被占用
**解决**: 
- 方法1: 关闭占用5000端口的程序
- 方法2: 修改`run.py`中的端口号为其他值(如8080)

### 问题4: 页面样式错乱
**解决**: 检查是否能访问CDN，或配置本地静态资源(参考DEPLOY.md)

### 问题5: 数据库初始化失败
**解决**: 
```bash
# 删除旧数据库
rm -rf database/dntest.db
# 重新初始化
python init_db.py
```

## 📚 进阶使用

### 配置静态资源CDN

编辑模板文件,将静态资源改为CDN链接:

```html
<!-- 使用CDN -->
<link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
```

### 修改系统配置

编辑 `config.py` 文件:

```python
# 修改系统名称
SYSTEM_NAME = '你的系统名称'

# 修改会话超时时间(小时)
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

# 关闭验证码
CAPTCHA_ENABLED = False
```

### 备份数据

```bash
# 备份数据库
cp database/dntest.db database/backup_$(date +%Y%m%d).db
```

### 恢复数据

```bash
# 恢复数据库
cp database/backup_20251203.db database/dntest.db
```

## 🎯 测试账号

系统预置了一个管理员账号:

| 用户名 | 密码 | 角色 | 权限 |
|--------|------|------|------|
| admin | admin123 | 超级管理员 | 全部权限 |

**安全提示**: 首次登录后请立即修改密码！

## 📞 获取帮助

- 查看 `README.md` - 项目说明
- 查看 `DEPLOY.md` - 详细部署指南  
- 查看 `PROJECT_SUMMARY.md` - 项目总结
- 查看日志文件 `logs/dntest.log`

## ✅ 检查清单

启动前确认:
- [ ] Python 3.8+ 已安装
- [ ] pip 可正常使用
- [ ] 端口5000未被占用
- [ ] 有足够的磁盘空间(> 100MB)

启动后确认:
- [ ] 浏览器能打开 http://localhost:5000
- [ ] 能看到登录页面
- [ ] 能用admin/admin123登录
- [ ] 能看到系统首页

全部确认后,系统即可正常使用！

---

**祝您使用愉快！** 🎉
