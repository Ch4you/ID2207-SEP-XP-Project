import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .db import db # 导入我们的内存数据库

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        user_data = db['users'].get(username) #

        if user_data is None:
            error = 'Incorrect username.'
        elif user_data['password'] != password: # 注意：真实项目中密码需要哈希
            error = 'Incorrect password.'

        if error is None:
            # 登录成功，信息存入 session
            session.clear()
            session['user_id'] = username
            session['user_role'] = user_data['role']
            session['user_name'] = user_data['name']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# 在每个请求之前加载登录的用户信息
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        user_data = db['users'].get(user_id) #
        if user_data:
            g.user = user_data.copy()
            g.user['username'] = user_id # 确保username在g.user中
        else:
            g.user = None
            session.clear() # 用户在数据库中不存在，清除session

# 登录装饰器 (用于保护页面)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# 角色检查装饰器 (用于实现HW4的访问控制)
def role_required(role_names): # 将参数名改为 role_names 以更好地表示可能是一个列表
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            # 检查角色是否匹配
            # 确保 role_names 始终是一个列表，以便进行一致的检查
            if not isinstance(role_names, list):
                allowed_roles = [role_names]
            else:
                allowed_roles = role_names

            if g.user['role'] not in allowed_roles:
                # 改进 flash 消息，以适应单个角色和多个角色的情况
                flash(f"Access denied. You must be one of the following roles: {', '.join(allowed_roles)}." if len(allowed_roles) > 1 else f"Access denied. You must be a {allowed_roles[0]}.", "error")
                return redirect(url_for('index')) # 重定向回主页
            return view(**kwargs)
        return wrapped_view # 修正：这里应该返回 wrapped_view 函数
    return decorator # 修正：这里应该返回实际的装饰器函数