"""
认证路由 - 登录、注册、登出
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, current_user
from app.models import db, User, LoginInfo, OnlineUser
from app.utils import get_client_ip, parse_user_agent, generate_session_id, success_response, error_response
import random
import string

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面和处理"""
    if current_user.is_authenticated:
        return redirect(url_for('main.system_index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('rememberme') == 'on'
        validate_code = request.form.get('validateCode', '').strip()
        
        # 验证码校验
        if current_app.config.get('CAPTCHA_ENABLED'):
            if not validate_code:
                return jsonify({'code': 500, 'msg': '请输入验证码'})
            
            if validate_code.lower() != session.get('captcha', '').lower():
                return jsonify({'code': 500, 'msg': '验证码错误'})
        
        # 查找用户
        user = User.query.filter_by(login_name=username, del_flag='0').first()
        
        if not user:
            log_login(username, '1', '用户不存在')
            return jsonify({'code': 500, 'msg': '用户名或密码错误'})
        
        # 检查用户状态
        if user.status != '0':
            log_login(username, '1', '账号已停用')
            return jsonify({'code': 500, 'msg': '账号已被停用，请联系管理员'})
        
        # 验证密码
        if not user.check_password(password):
            log_login(username, '1', '密码错误')
            return jsonify({'code': 500, 'msg': '用户名或密码错误'})
        
        # 登录成功
        login_user(user, remember=remember)
        
        # 更新用户登录信息
        user.login_ip = get_client_ip()
        user.login_date = datetime.now()
        db.session.commit()
        
        # 记录登录日志
        log_login(username, '0', '登录成功')
        
        # 记录在线用户
        record_online_user(user)
        
        return jsonify({'code': 0, 'msg': '登录成功'})
    
    # GET请求 - 显示登录页面
    captcha_enabled = current_app.config.get('CAPTCHA_ENABLED', True)
    is_remembered = current_app.config.get('REMEMBER_ME_ENABLED', True)
    is_register = current_app.config.get('REGISTER_ENABLED', False)
    
    return render_template('login.html',
                         captchaEnabled=captcha_enabled,
                         captchaType='math',  # math或char
                         isRemembered=is_remembered,
                         isAllowRegister=is_register)


@auth_bp.route('/logout')
def logout():
    """登出"""
    if current_user.is_authenticated:
        # 删除在线用户记录
        OnlineUser.query.filter_by(login_name=current_user.login_name).delete()
        db.session.commit()
    
    logout_user()
    flash('您已成功登出系统', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/captcha/captchaImage')
def captcha_image():
    """生成验证码图片"""
    from io import BytesIO
    from flask import make_response
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        use_pil = True
    except ImportError:
        use_pil = False
    
    # 生成随机验证码
    captcha_type = request.args.get('type', 'math')
    
    if captcha_type == 'math':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operators = ['+', '-']
        operator = random.choice(operators)
        
        if operator == '+':
            result = num1 + num2
        else:
            result = num1 - num2
            if result < 0:
                num1, num2 = num2, num1
                result = num1 - num2
        
        captcha_text = f"{num1}{operator}{num2}="
        captcha_value = str(result)
    else:
        length = current_app.config.get('CAPTCHA_LENGTH', 4)
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        captcha_value = captcha_text
    
    # 保存到session
    session['captcha'] = captcha_value
    
    if not use_pil:
        # 如果PIL不可用，返回简单的SVG验证码
        svg = f'''<svg width="120" height="40" xmlns="http://www.w3.org/2000/svg">
            <rect width="120" height="40" fill="white"/>
            <text x="10" y="28" font-family="Arial" font-size="20" fill="black">{captcha_text}</text>
            <line x1="0" y1="20" x2="120" y2="20" stroke="gray" stroke-width="1" opacity="0.3"/>
            <line x1="60" y1="0" x2="60" y2="40" stroke="gray" stroke-width="1" opacity="0.3"/>
        </svg>'''
        response = make_response(svg)
        response.headers['Content-Type'] = 'image/svg+xml'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    
    # 使用PIL创建图片
    width, height = 120, 40
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 绘制干扰线
    for _ in range(3):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill='gray', width=1)
    
    # 绘制文字
    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except:
        font = ImageFont.load_default()
    
    # 绘制验证码文字
    text_width = draw.textlength(captcha_text, font=font) if hasattr(draw, 'textlength') else len(captcha_text) * 15
    x = (width - text_width) / 2
    y = (height - 24) / 2
    
    draw.text((x, y), captcha_text, fill='black', font=font)
    
    # 添加干扰点
    for _ in range(100):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill='gray')
    
    # 输出图片
    buf = BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    if not current_app.config.get('REGISTER_ENABLED'):
        flash('系统未开放注册功能', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # 注册逻辑
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # 验证用户名是否已存在
        if User.query.filter_by(login_name=username).first():
            return jsonify({'code': 500, 'msg': '用户名已存在'})
        
        # 创建新用户
        user = User(
            login_name=username,
            user_name=username,
            status='0',
            create_time=datetime.now()
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '注册成功'})
    
    return render_template('register.html')


def log_login(login_name, status, msg):
    """记录登录日志"""
    ip = get_client_ip()
    browser, os = parse_user_agent(request.headers.get('User-Agent', ''))
    
    log = LoginInfo(
        login_name=login_name,
        ipaddr=ip,
        login_location='',  # 可以集成IP定位服务
        browser=browser,
        os=os,
        status=status,
        msg=msg,
        login_time=datetime.now()
    )
    
    db.session.add(log)
    db.session.commit()


def record_online_user(user):
    """记录在线用户"""
    session_id = generate_session_id()
    ip = get_client_ip()
    browser, os = parse_user_agent(request.headers.get('User-Agent', ''))
    
    # 删除旧的在线记录
    OnlineUser.query.filter_by(login_name=user.login_name).delete()
    
    # 创建新记录
    online_user = OnlineUser(
        sessionId=session_id,
        login_name=user.login_name,
        dept_name=user.dept.dept_name if user.dept else '',
        ipaddr=ip,
        login_location='',
        browser=browser,
        os=os,
        status='on_line',
        start_timestamp=datetime.now(),
        last_access_time=datetime.now(),
        expire_time=120  # 2小时
    )
    
    db.session.add(online_user)
    db.session.commit()
