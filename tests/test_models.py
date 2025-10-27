from app.models import EventPlanningRequest
import pytest

def test_event_request_creation_and_submit():
    # 你们的第一个TDD测试 [cite: 92]
    req = EventPlanningRequest(
        client_name="Test Client",
        event_type="Conference",
        from_date="2025-11-01",
        to_date="2025-11-03",
        expected_attendees=100,
        preferences=["Food", "Music"],
        expected_budget=50000,
        created_by="sarah"
    )
    
    # 1. 测试初始状态 (来自HW3 State Chart [cite: 304])
    assert req.status == "Draft"
    
    # 2. 执行动作
    req.submit() # [cite: 305]
    
    # 3. 测试结果状态 (来自HW3 State Chart [cite: 306])
    assert req.status == "Submitted"
    
    # 4. 测试非法状态转换
    with pytest.raises(Exception):
        req.submit() # 不能重复提交

def test_request_routing():
    # 第二个TDD测试 [cite: 92]
    req = EventPlanningRequest(
        client_name="Test Client",
        event_type="Workshop",
        from_date="2025-12-01",
        to_date="2025-12-01",
        expected_attendees=30,
        preferences=[],
        expected_budget=10000,
        created_by="sarah"
    )
    
    # 必须先提交 [cite: 305]
    req.submit()
    assert req.status == "Submitted"
    
    # 执行路由动作 (来自HW3 State Chart [cite: 307])
    req.route_to_senior_officer()
    assert req.status == "UnderReview" # [cite: 308]