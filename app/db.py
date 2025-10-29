# 这是一个简单的Python字典，充当你们的内存数据库
# 它将在程序关闭时丢失，这符合项目要求
from app.models import EventPlanningRequest, Task, StaffingRequest, FinancialRequest

# ==================================
# 1. 用户数据
# ==================================
# 所有用户和角色均来自 Business Case
users = {
    # Customer Service Team
    "sarah": {"password": "123", "role": "CustomerServiceOfficer", "name": "Sarah"}, #
    "sam": {"password": "123", "role": "CustomerServiceOfficer", "name": "Sam"}, #
    "janet": {"password": "123", "role": "SeniorCustomerServiceOfficer", "name": "Janet (SCS)"}, #

    # Management
    "mike": {"password": "123", "role": "AdministrationManager", "name": "Mike (AM)"}, #
    "alice": {"password": "123", "role": "FinancialManager", "name": "Alice (FM)"}, #

    # Production & Service Managers
    "jack": {"password": "123", "role": "ProductionManager", "name": "Jack (PM)"}, #
    "natalie": {"password": "123", "role": "ServiceManager", "name": "Natalie (SM)"}, #

    # HR Team
    "simon": {"password": "123", "role": "HRTeam", "name": "Simon (HR)"}, #
    "maria": {"password": "123", "role": "HRTeam", "name": "Maria (HR Assistant)"}, #

    # Sub-teams (简化：我们只添加了领导)
    "magy": {"password": "123", "role": "SubTeamLeader", "name": "Magy (Decorations)"}, #
    "helen": {"password": "123", "role": "SubTeamLeader", "name": "Helen (Top Chef)"}, #
    "tobi": {"password": "123", "role": "SubTeamLeader", "name": "Tobias (Photographer)"} #
}

# ==================================
# 2. 示例数据 - 让仪表盘看起来有内容
# ==================================

# --- 事件请求 (Event Requests) ---

# 请求 1: 等待 SCS (Janet) 审核
req1 = EventPlanningRequest("KTH Royal Institute", "Workshop", "2025-11-15", "2025-11-16", 50, ["Food", "Network Support"], 25000, "sarah")
req1.submit()
req1.route_to_senior_officer() # -> UnderReview

# 请求 2: 等待 AM (Mike) 最终批准
req2 = EventPlanningRequest("Ericsson AB", "Conference", "2025-12-01", "2025-12-03", 200, ["Decorations", "Filming", "Food", "Drinks"], 150000, "sam")
req2.submit()
req2.route_to_senior_officer()
req2.forward_for_decision("SCS/FM: Budget looks reasonable") # -> Approved

# 请求 3: 已批准并进行中 (用于生成任务和请求)
req3 = EventPlanningRequest("Music College", "Concert", "2025-11-20", "2025-11-20", 300, ["Audio", "Decorations", "Drinks"], 80000, "sarah")
req3.submit()
req3.route_to_senior_officer()
req3.forward_for_decision("SCS/FM: Looks good")
req3.approve("AM: Approved for execution") # -> InProgress

# 请求 4: 另一个等待 SCS (Janet) 审核
req4 = EventPlanningRequest("Spotify HQ", "Team Building Event", "2025-11-25", "2025-11-25", 80, ["Food", "Parties", "Audio"], 40000, "sam")
req4.submit()
req4.route_to_senior_officer() # -> UnderReview

# 请求 5: 另一个已批准并进行中
req5 = EventPlanningRequest("Stockholm University", "Summer School", "2026-07-10", "2026-07-17", 120, ["Food", "Drinks", "Filming"], 95000, "sarah")
req5.submit()
req5.route_to_senior_officer()
req5.forward_for_decision("Budget OK")
req5.approve("Approved") # -> InProgress

# 请求 6: 一个已被拒绝的请求
req6 = EventPlanningRequest("Small Startup Inc.", "Product Launch", "2025-11-05", "2025-11-05", 30, ["Drinks"], 5000, "sam")
req6.submit()
req6.route_to_senior_officer()
req6.reject("AM: Budget too low for requested scope.") # -> Rejected

# --- 任务 (Tasks) ---

# 与 req3 (Music Concert) 相关
task1 = Task(req3.id, "Stage Decorations", "Classical music theme, blue and gold colors.", "Decorations", "jack")
task1.assign() # -> Assigned

task2 = Task(req3.id, "VIP Catering", "Prepare snacks and drinks for 50 VIP guests.", "Chef", "natalie")
task2.assign() # -> Assigned

task3 = Task(req3.id, "Audio Setup", "Set up microphones and speakers for live orchestra.", "Audio", "jack") # (假设有Audio团队)
task3.assign() # -> Assigned

# 与 req5 (Summer School) 相关
task4 = Task(req5.id, "Daily Lunch Buffet", "International cuisine for 120 attendees daily.", "Chef", "natalie")
task4.assign() # -> Assigned

task5 = Task(req5.id, "Lecture Filming", "Record all lectures and provide edited videos.", "Photographer", "jack")
task5.assign() # -> Assigned

# --- 人员请求 (Staffing Requests) ---

# 请求 1: 等待 HR (Simon/Maria) 处理 (来自 req3)
staff_req1 = StaffingRequest(req3.id, "Production", "Lighting Technician", "Need temporary staff for concert lighting setup.", "jack")
# (状态默认为 Submitted)

# 请求 2: 另一个等待 HR 处理 (来自 req5)
staff_req2 = StaffingRequest(req5.id, "Services", "Waiter", "Need 5 additional waiters for the duration of the summer school.", "natalie")
# (状态默认为 Submitted)

# --- 财务请求 (Financial Requests) ---

# 请求 1: 等待 FM (Alice) 处理 (来自 req3)
fin_req1 = FinancialRequest(req3.id, "Production", 7500, "Need to rent special vintage microphones for audio team.", "jack")
# (状态默认为 Submitted)

# 请求 2: 另一个等待 FM 处理 (来自 req5)
fin_req2 = FinancialRequest(req5.id, "Services", 3000, "Additional budget for premium coffee beans requested by client.", "natalie")
# (状态默认为 Submitted)


# ==================================
# 3. 数据库字典
# ==================================
db = {
    "users": users,
    "event_requests": [req1, req2, req3, req4, req5, req6],
    "staffing_requests": [staff_req1, staff_req2],
    "financial_requests": [fin_req1, fin_req2],
    "tasks": [task1, task2, task3, task4, task5]
}

# ==================================
# 4. 辅助函数 - 用于通过ID查找
# ==================================
def get_request_by_id(req_id):
    # Ensure req_id is an integer
    try:
        req_id = int(req_id)
    except ValueError:
        return None
        
    for req in db['event_requests']:
        if req.id == req_id:
            return req
    return None

def get_task_by_id(task_id):
    # Ensure task_id is an integer
    try:
        task_id = int(task_id)
    except ValueError:
        return None

    for task in db['tasks']:
        if task.id == task_id:
            return task
    return None

def get_staffing_request_by_id(req_id):
    # Ensure req_id is an integer
    try:
        req_id = int(req_id)
    except ValueError:
        return None

    for req in db['staffing_requests']:
        if req.id == req_id:
            return req
    return None

def get_financial_request_by_id(req_id):
    # Ensure req_id is an integer
    try:
        req_id = int(req_id)
    except ValueError:
        return None

    for req in db['financial_requests']:
        if req.id == req_id:
            return req
    return None