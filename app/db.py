# 这是一个简单的Python字典，充当你们的内存数据库
# 它将在程序关闭时丢失，这符合项目要求

# 所有用户和角色均来自 Business Case
db = {
    "users": {
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
    },
    "event_requests": [],
    "staffing_requests": [],
    "financial_requests": [],
    "tasks": []
}

# 辅助函数，用于通过ID查找
def get_request_by_id(req_id):
    for req in db['event_requests']:
        if req.id == req_id:
            return req
    return None

def get_task_by_id(task_id):
    for task in db['tasks']:
        if task.id == task_id:
            return task
    return None

def get_staffing_request_by_id(req_id):
    for req in db['staffing_requests']:
        if req.id == req_id:
            return req
    return None
    
def get_financial_request_by_id(req_id):
    for req in db['financial_requests']:
        if req.id == req_id:
            return req
    return None