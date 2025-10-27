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
def role_required(role_name):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            # 检查角色是否匹配
            if g.user['role'] != role_name:
                flash(f"Access denied. You must be a {role_name}.")
                return redirect(url_for('index')) # 重定向回主页
            return view(**kwargs)
        return decorator
    return role_required