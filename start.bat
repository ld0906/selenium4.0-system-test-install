@echo off
echo ====================================
echo  大牛测试系统 - Windows启动脚本
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)

echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [3/4] 安装依赖...
chcp 65001 >nul
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [4/4] 检查数据库...
if not exist "database\dntest.db" (
    echo 初始化数据库...
    python init_db.py
)

echo.
echo ====================================
echo  启动应用服务器...
echo  访问地址: http://localhost:5000
echo  默认账号: admin / admin123
echo ====================================
echo.

python run.py

pause
