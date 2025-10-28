from app.models import EventPlanningRequest, Task, Plan, StaffingRequest, FinancialRequest
import pytest

# ==================================
# 1. EventPlanningRequest TDD
# (基于 HW3 Figure 6)
# ==================================

@pytest.fixture
def event_req():
    """返回一个干净的、处于 Draft 状态的 EventRequest"""
    return EventPlanningRequest(
        client_name="Test Client", event_type="Conference", from_date="2025-11-01",
        to_date="2025-11-03", expected_attendees=100, preferences=["Food"],
        expected_budget=50000, created_by="sarah"
    )

def test_event_full_workflow(event_req):
    # 1. Draft -> Submitted
    assert event_req.status == "Draft"
    event_req.submit()
    assert event_req.status == "Submitted"

    # 2. Submitted -> UnderReview
    event_req.route_to_senior_officer()
    assert event_req.status == "UnderReview"

    # 3. UnderReview -> Approved (by FM/SCS)
    event_req.forward_for_decision("FM looks good")
    assert event_req.status == "Approved"
    assert event_req.feedback_fm == "FM looks good"

    # 4. Approved -> InProgress (by AM)
    event_req.approve("AM says go")
    assert event_req.status == "InProgress"
    assert event_req.feedback_am == "AM says go"
    
    # 5. InProgress -> Closed
    event_req.finalize()
    assert event_req.status == "Closed"

def test_event_rejection_workflow(event_req):
    event_req.submit()
    event_req.route_to_senior_officer()
    assert event_req.status == "UnderReview"
    
    # UnderReview -> Rejected
    event_req.reject("AM rejected")
    assert event_req.status == "Rejected"
    assert event_req.feedback_am == "AM rejected"

def test_event_return_workflow(event_req):
    event_req.submit()
    event_req.route_to_senior_officer()
    assert event_req.status == "UnderReview"
    
    # UnderReview -> Draft
    event_req.return_for_completion("Needs more details")
    assert event_req.status == "Draft"
    assert event_req.feedback_fm == "Needs more details"

# ==================================
# 2. Task & Plan TDD

# ==================================

@pytest.fixture
def task():
    """返回一个干净的、处于 Created 状态的 Task"""
    return Task(
        event_request_id=1, title="Decorations",
        description="Music theme", assigned_to_team="Decorations",
        created_by="jack"
    )

def test_task_workflow(task):
    # 1. Created -> Assigned
    assert task.status == "Created"
    task.assign()
    assert task.status == "Assigned"

    # 2. Assigned -> Planned
    plan = Plan(details="Roses and blue lights", resources_needed="5 staff", budget_needs=5000, submitted_by="magy")
    task.submit_plan(plan)
    assert task.status == "Planned"
    assert task.plan is not None
    assert task.plan.budget_needs == 5000

    # 3. Planned -> Completed
    task.mark_complete()
    assert task.status == "Completed"

# ==================================
# 3. StaffingRequest TDD
# ==================================

@pytest.fixture
def staff_req():
    """返回一个干净的、处于 Submitted 状态的 StaffingRequest"""
    return StaffingRequest(
        event_request_id=1, department="Production", job_title="Photographer",
        job_description="Need one more", requested_by="jack"
    )

def test_staffing_workflow_resolve(staff_req):
    assert staff_req.status == "Submitted"
    
    # Submitted -> Resolved (via Hiring)
    staff_req.process(decision="Hiring", feedback="Approved, will post job")
    assert staff_req.status == "Resolved"
    assert staff_req.hr_decision == "Hiring"
    
    # Test invalid transition
    with pytest.raises(ValueError):
        staff_req.process("Rejected", "Too late")

def test_staffing_workflow_reject(staff_req):
    assert staff_req.status == "Submitted"
    
    # Submitted -> Rejected
    staff_req.process(decision="Rejected", feedback="No budget")
    assert staff_req.status == "Rejected"
    assert staff_req.hr_decision == "Rejected"

# ==================================
# 4. FinancialRequest TDD
# ==================================

@pytest.fixture
def fin_req():
    """返回一个干净的、处于 Submitted 状态的 FinancialRequest"""
    return FinancialRequest(
        event_request_id=1, department="Production", required_amount=5000,
        reason="Need better lights", requested_by="jack"
    )

def test_financial_workflow_approve(fin_req):
    assert fin_req.status == "Submitted"
    fin_req.approve("OK, but be careful")
    assert fin_req.status == "Approved"
    assert fin_req.fm_feedback == "OK, but be careful"

def test_financial_workflow_reject(fin_req):
    assert fin_req.status == "Submitted"
    fin_req.reject("No budget left")
    assert fin_req.status == "Rejected"
    assert fin_req.fm_feedback == "No budget left"