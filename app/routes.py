from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
# (从 auth 导入装饰器，用于保护路由)
from app.auth import login_required, role_required
# (从 db 导入内存数据库和辅助函数)
from .db import db, get_request_by_id, get_task_by_id, get_staffing_request_by_id, get_financial_request_by_id
# (导入所有模型类)
from app.models import EventPlanningRequest, Task, Plan, StaffingRequest, FinancialRequest

bp = Blueprint('main', __name__)

@bp.before_app_request
def load_db_and_user():
    # 将内存数据库和用户加载到g，以便在所有模板中访问
    g.db = db # 将内存数据库加载到g
    # g.user 已经由 auth.load_logged_in_user 加载，无需在此处重复加载用户逻辑。


# ====================================================================
# 1. 仪表盘
# ====================================================================

@bp.route('/')
@login_required
def index():
    # 主页/仪表盘
    # (根据角色过滤列表，以便在仪表盘上显示 "待办事项")
    role = g.user['role']
    my_tasks = []
    
    if role == 'SeniorCustomerServiceOfficer':
        # SCS (Janet) 看到 "UnderReview" 的请求
        my_tasks = [req for req in db['event_requests'] if req.status == 'UnderReview']
    elif role == 'AdministrationManager':
        # AM (Mike) 看到 "Approved" (待启动) 的请求
        my_tasks = [req for req in db['event_requests'] if req.status == 'Approved']
    elif role == 'FinancialManager':
        # FM (Alice) 看到待处理的财务请求
        my_tasks = [req for req in db['financial_requests'] if req.status == 'Submitted']
    elif role == 'HRTeam':
        # HR (Simon) 看到待处理的招聘请求
        my_tasks = [req for req in db['staffing_requests'] if req.status == 'Submitted']
    elif role == 'SubTeamLeader':
        # SubTeam (Magy, Helen) 看到 "Assigned" 给他们的任务
        my_tasks = [t for t in db['tasks'] if t.status == 'Assigned' and t.assigned_to_team == g.user['name'].split(' ')[0]]
        
    return render_template('main/dashboard.html', my_tasks=my_tasks)


# ====================================================================
# 2. 工作流 1: Event Request
# ====================================================================

@bp.route('/request/new', methods=('GET', 'POST'))
@login_required
@role_required('CustomerServiceOfficer') #
def create_event_request():
    if request.method == 'POST':
        # (来自 create_request.html 表单)
        preferences = request.form.getlist('preferences') # 获取复选框列表

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
        
        new_req.submit() #
        new_req.route_to_senior_officer() #
        
        db['event_requests'].append(new_req)
        
        flash(f"Event Request for {new_req.client_name} created and routed to Senior Officer.", "success")
        return redirect(url_for('index'))

    return render_template('main/create_event_request.html') #

@bp.route('/request/<int:req_id>')
@login_required
def event_request_detail(req_id):
    req = get_request_by_id(req_id)
    if not req: abort(404)
    return render_template('main/event_request_detail.html', req=req)

@bp.route('/request/<int:req_id>/action', methods=('POST',))
@login_required
def event_request_action(req_id):
    req = get_request_by_id(req_id)
    if not req: abort(404)
    
    action = request.form['action']
    feedback = request.form['feedback']
    role = g.user['role']

    try:
        # (SCS 或 FM 的审批逻辑)
        if action == 'forward_to_am' and role in ['SeniorCustomerServiceOfficer', 'FinancialManager']:
            req.forward_for_decision(feedback)
            flash('Request forwarded to Administration Manager.', 'success')
            
        # (AM 的最终审批)
        elif action == 'approve' and role == 'AdministrationManager':
            req.approve(feedback) # 
            flash('Event Approved and moved to InProgress.', 'success')

        # (任何人都可以拒绝)
        elif action == 'reject':
            req.reject(feedback) #
            flash('Event Rejected.', 'error')
            
        elif action == 'finalize' and role in ['AdministrationManager', 'SeniorCustomerServiceOfficer']:
            req.finalize() #
            flash('Event finalized and Closed.', 'success')
            
        else:
            flash('Invalid action for your role.', 'error')
            
    except Exception as e:
        flash(f'Action failed: {e}', 'error')

    return redirect(url_for('main.event_request_detail', req_id=req_id))


# ====================================================================
# 3. 工作流 2: Task Distribution
# ====================================================================

@bp.route('/event/<int:event_id>/task/new', methods=('GET', 'POST'))
@login_required
@role_required(['ProductionManager', 'ServiceManager']) #
def create_task(event_id):
    event_req = get_request_by_id(event_id)
    if not event_req: abort(404)
    
    if request.method == 'POST':
        task = Task(
            event_request_id=event_id,
            title=request.form['title'],
            description=request.form['description'],
            assigned_to_team=request.form['assigned_to_team'],
            created_by=g.user['username']
        )
        task.assign() #
        db['tasks'].append(task)
        flash(f"Task '{task.title}' created and assigned to {task.assigned_to_team}.", 'success')
        return redirect(url_for('main.event_request_detail', req_id=event_id))

    return render_template('main/create_task.html', event_req=event_req)

@bp.route('/task/<int:task_id>', methods=('GET', 'POST'))
@login_required
@role_required('SubTeamLeader') #
def task_detail(task_id):
    task = get_task_by_id(task_id)
    if not task: abort(404)
    
    if request.method == 'POST':
        # (子团队提交他们的计划)
        try:
            plan = Plan(
                details=request.form['details'],
                resources_needed=request.form['resources_needed'],
                budget_needs=float(request.form['budget_needs']),
                submitted_by=g.user['name']
            )
            task.submit_plan(plan) #
            flash(f"Plan for '{task.title}' submitted.", 'success')
        except Exception as e:
            flash(f'Action failed: {e}', 'error')
        return redirect(url_for('main.task_detail', task_id=task_id))
        
    return render_template('main/task_detail.html', task=task)


# ====================================================================
# 4. 工作流 3: Staffing Request
# ====================================================================

@bp.route('/event/<int:event_id>/staffing/new', methods=('GET', 'POST'))
@login_required
@role_required(['ProductionManager', 'ServiceManager']) #
def create_staffing_request(event_id):
    if request.method == 'POST':
        req = StaffingRequest(
            event_request_id=event_id,
            department=request.form['department'], #
            job_title=request.form['job_title'], #
            job_description=request.form['job_description'], #
            requested_by=g.user['username']
        )
        db['staffing_requests'].append(req)
        flash(f"Staffing Request for {req.job_title} submitted to HR.", 'success')
        return redirect(url_for('main.event_request_detail', req_id=event_id))

    return render_template('main/create_staffing_request.html', event_id=event_id)

@bp.route('/staffing/<int:req_id>', methods=('GET', 'POST'))
@login_required
@role_required(['HRTeam', 'ProductionManager', 'ServiceManager']) # 
def staffing_request_detail(req_id):
    req = get_staffing_request_by_id(req_id)
    if not req: abort(404)
    
    if request.method == 'POST' and g.user['role'] == 'HRTeam': #
        try:
            req.process( #
                decision=request.form['decision'],
                feedback=request.form['feedback']
            )
            flash("Staffing request processed.", 'success')
        except Exception as e:
            flash(f'Action failed: {e}', 'error')
        return redirect(url_for('main.staffing_request_detail', req_id=req_id))
        
    return render_template('main/staffing_request_detail.html', req=req)


# ====================================================================
# 5. 工作流 4: Financial Request
# ====================================================================

@bp.route('/event/<int:event_id>/financial/new', methods=('GET', 'POST'))
@login_required
@role_required(['ProductionManager', 'ServiceManager']) #
def create_financial_request(event_id):
    if request.method == 'POST':
        req = FinancialRequest(
            event_request_id=event_id,
            department=request.form['department'], #
            required_amount=float(request.form['required_amount']), #
            reason=request.form['reason'], #
            requested_by=g.user['username']
        )
        db['financial_requests'].append(req)
        flash(f"Financial Request for {req.required_amount} SEK submitted to FM.", 'success')
        return redirect(url_for('main.event_request_detail', req_id=event_id))

    return render_template('main/create_financial_request.html', event_id=event_id)

@bp.route('/financial/<int:req_id>', methods=('GET', 'POST'))
@login_required
@role_required(['FinancialManager', 'ProductionManager', 'ServiceManager']) #
def financial_request_detail(req_id):
    req = get_financial_request_by_id(req_id)
    if not req: abort(404)
    
    if request.method == 'POST' and g.user['role'] == 'FinancialManager': #
        try:
            feedback = request.form['feedback']
            if request.form['action'] == 'approve':
                req.approve(feedback)
                flash("Financial request approved.", 'success')
            else:
                req.reject(feedback)
                flash("Financial request rejected.", 'error')
        except Exception as e:
            flash(f'Action failed: {e}', 'error')
        return redirect(url_for('main.financial_request_detail', req_id=req_id))
        
    return render_template('main/financial_request_detail.html', req=req)