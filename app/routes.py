from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from app.auth import login_required, role_required
from app.models import EventPlanningRequest
from .db import db

bp = Blueprint('main', __name__)

@bp.before_app_request
def load_db():
    # 将内存数据库加载到g，以便在模板中访问
    g.db = db

@bp.route('/')
@login_required
def index():
    # 主页/仪表盘
    # [cite: 89] (不同角色看到不同功能)
    return render_template('main/dashboard.html')

@bp.route('/request/new', methods=('GET', 'POST'))
@login_required
@role_required('CustomerServiceOfficer') # 只有CustomerServiceOfficer能访问 [cite: 861, 1159]
def create_request():
    if request.method == 'POST':
        # 从 request.form 获取数据 
        preferences = []
        if request.form.get('pref_decorations'): preferences.append('Decorations')
        if request.form.get('pref_parties'): preferences.append('Parties')
        if request.form.get('pref_photos'): preferences.append('Photos/Filming')
        if request.form.get('pref_breakfast'): preferences.append('Breakfast/Lunch/Dinner')
        if request.form.get('pref_drinks'): preferences.append('Soft/Hot Drinks')

        new_req = EventPlanningRequest(
            client_name=request.form['client_name'],
            event_type=request.form['event_type'],
            from_date=request.form['from_date'],
            to_date=request.form['to_date'],
            expected_attendees=request.form['expected_attendees'],
            preferences=preferences,
            expected_budget=request.form['expected_budget'],
            created_by=g.user['username']
        )
        
        # TDD的核心逻辑
        new_req.submit() # [cite: 305]
        new_req.route_to_senior_officer() # [cite: 307]
        
        # 存入"数据库" [cite: 86]
        db['event_requests'].append(new_req)
        
        flash(f"Event Request for {new_req.client_name} created and routed to Senior Officer.")
        return redirect(url_for('index'))

    # GET 请求，显示表单 [cite: 87, 864]
    return render_template('main/create_request.html')