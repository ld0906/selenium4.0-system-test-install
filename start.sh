#!/bin/bash

echo "===================================="
echo " 大牛测试系统 - Linux启动脚本"
echo "===================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "[1/4] 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "[2/4] 激活虚拟环境..."
source venv/bin/activate

echo "[3/4] 安装依赖..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "[4/4] 检查数据库..."
if [ ! -f "database/dntest.db" ]; then
    echo "初始化数据库..."
    python init_db.py
fi

echo ""
echo "===================================="
echo " 启动应用服务器..."
echo " 访问地址: http://localhost:5000"
echo " 默认账号: admin / admin123"
echo "===================================="
echo ""

python run.py
