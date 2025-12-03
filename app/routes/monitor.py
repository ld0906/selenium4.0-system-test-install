"""
系统监控路由 - 在线用户、定时任务、操作日志、登录日志、服务监控
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models import db, OnlineUser, Job, JobLog, OperLog, LoginInfo
from app.decorators import permission_required
from app.utils import table_response, paginate, success_response, error_response
import psutil
from datetime import datetime

monitor_bp = Blueprint('monitor', __name__)


@monitor_bp.route('/online/list')
@login_required
@permission_required('monitor:online:view')
def online_list():
    """在线用户列表页面"""
    return render_template('monitor/online/online.html')


@monitor_bp.route('/online/list/data')
@login_required
@permission_required('monitor:online:list')
def online_list_data():
    """在线用户列表数据"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    
    query = OnlineUser.query.filter_by(status='on_line')
    users, total = paginate(query.order_by(OnlineUser.last_access_time.desc()), page, per_page)
    
    rows = []
    for user in users:
        row = {
            'sessionId': user.sessionId,
            'login_name': user.login_name,
            'dept_name': user.dept_name,
            'ipaddr': user.ipaddr,
            'login_location': user.login_location,
            'browser': user.browser,
            'os': user.os,
            'status': user.status,
            'start_timestamp': user.start_timestamp.strftime('%Y-%m-%d %H:%M:%S') if user.start_timestamp else '',
            'last_access_time': user.last_access_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_access_time else ''
        }
        rows.append(row)
    
    return table_response(rows, total)


@monitor_bp.route('/job/list')
@login_required
@permission_required('monitor:job:view')
def job_list():
    """定时任务列表页面"""
    return render_template('monitor/job/job.html')


@monitor_bp.route('/operlog/list')
@login_required
@permission_required('monitor:operlog:view')
def operlog_list():
    """操作日志列表页面"""
    return render_template('monitor/operlog/operlog.html')


@monitor_bp.route('/operlog/list/data')
@login_required
@permission_required('monitor:operlog:list')
def operlog_list_data():
    """操作日志列表数据"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    
    query = OperLog.query
    logs, total = paginate(query.order_by(OperLog.oper_time.desc()), page, per_page)
    
    rows = []
    for log in logs:
        row = {
            'oper_id': log.oper_id,
            'title': log.title,
            'business_type': log.business_type,
            'request_method': log.request_method,
            'oper_name': log.oper_name,
            'dept_name': log.dept_name,
            'oper_url': log.oper_url,
            'oper_ip': log.oper_ip,
            'oper_location': log.oper_location,
            'status': log.status,
            'oper_time': log.oper_time.strftime('%Y-%m-%d %H:%M:%S') if log.oper_time else ''
        }
        rows.append(row)
    
    return table_response(rows, total)


@monitor_bp.route('/logininfor/list')
@login_required
@permission_required('monitor:logininfor:view')
def logininfor_list():
    """登录日志列表页面"""
    return render_template('monitor/logininfor/logininfor.html')


@monitor_bp.route('/logininfor/list/data')
@login_required
@permission_required('monitor:logininfor:list')
def logininfor_list_data():
    """登录日志列表数据"""
    page = request.args.get('pageNum', 1, type=int)
    per_page = request.args.get('pageSize', 10, type=int)
    
    query = LoginInfo.query
    logs, total = paginate(query.order_by(LoginInfo.login_time.desc()), page, per_page)
    
    rows = []
    for log in logs:
        row = {
            'info_id': log.info_id,
            'login_name': log.login_name,
            'ipaddr': log.ipaddr,
            'login_location': log.login_location,
            'browser': log.browser,
            'os': log.os,
            'status': log.status,
            'msg': log.msg,
            'login_time': log.login_time.strftime('%Y-%m-%d %H:%M:%S') if log.login_time else ''
        }
        rows.append(row)
    
    return table_response(rows, total)


@monitor_bp.route('/server')
@login_required
@permission_required('monitor:server:view')
def server():
    """服务器监控页面"""
    return render_template('monitor/server/server.html')


@monitor_bp.route('/server/info')
@login_required
@permission_required('monitor:server:list')
def server_info():
    """获取服务器信息"""
    try:
        # CPU信息
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存信息
        mem = psutil.virtual_memory()
        mem_total = mem.total / (1024 ** 3)  # GB
        mem_used = mem.used / (1024 ** 3)
        mem_free = mem.free / (1024 ** 3)
        mem_percent = mem.percent
        
        # 磁盘信息
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024 ** 3)
        disk_used = disk.used / (1024 ** 3)
        disk_free = disk.free / (1024 ** 3)
        disk_percent = disk.percent
        
        server_info = {
            'cpu': {
                'count': cpu_count,
                'count_logical': cpu_count_logical,
                'percent': cpu_percent
            },
            'memory': {
                'total': round(mem_total, 2),
                'used': round(mem_used, 2),
                'free': round(mem_free, 2),
                'percent': mem_percent
            },
            'disk': {
                'total': round(disk_total, 2),
                'used': round(disk_used, 2),
                'free': round(disk_free, 2),
                'percent': disk_percent
            },
            'python_version': psutil.python_version() if hasattr(psutil, 'python_version') else 'N/A',
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return success_response(data=server_info)
    except Exception as e:
        return error_response(f'获取服务器信息失败: {str(e)}')
