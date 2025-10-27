# 这是一个简单的Python字典，充当你们的内存数据库
# 它将在程序关闭时丢失，这符合项目要求 
db = {
    "users": {
        "sarah": {"password": "123", "role": "CustomerServiceOfficer", "name": "Sarah"},
        "janet": {"password": "123", "role": "SeniorCustomerServiceOfficer", "name": "Janet"},
        "alice": {"password": "123", "role": "FinancialManager", "name": "Alice"},
        "mike": {"password": "123", "role": "AdministrationManager", "name": "Mike"},
        "jack": {"password": "123", "role": "ProductionManager", "name": "Jack"},
        "simon": {"password": "123", "role": "HRTeam", "name": "Simon"}
    },
    "event_requests": [],
    "staffing_requests": [],
    "financial_requests": []
}