import datetime

# ====================================================================
# 工作流 1: Event Planning Request
# ====================================================================

class EventPlanningRequest:
    """
    Represents an Event Planning Request, tracking its state and details.
    # 状态和转换基于 HW3 State Chart Diagram (Figure 6)
    """
    _id_counter = 1

    def __init__(self, client_name, event_type, from_date, to_date, expected_attendees, preferences, expected_budget, created_by):
        self.id = EventPlanningRequest._id_counter
        EventPlanningRequest._id_counter += 1
        
        self.client_name = client_name
        self.event_type = event_type
        self.from_date = from_date
        self.to_date = to_date
        self.expected_attendees = expected_attendees
        self.preferences = preferences
        self.expected_budget = expected_budget
        self.created_by = created_by
        
        self.status = "Draft" # 
        self.feedback_fm = None # 财务经理的反馈
        self.feedback_am = None # 行政经理的反馈

    def submit(self):
        # Action: submit()
        if self.status == "Draft":
            self.status = "Submitted"
        else:
            raise ValueError("Only Draft requests can be submitted.")
            
    def route_to_senior_officer(self):
        # Action: routeToSeniorOfficer(request)
        if self.status == "Submitted":
            self.status = "UnderReview"
        else:
            raise ValueError("Only Submitted requests can be routed.")

    def return_for_completion(self, feedback):
        # Action: returnForCompletion()
        if self.status == "UnderReview":
            self.status = "Draft"
            self.feedback_fm = feedback
        else:
            raise ValueError("Only requests UnderReview can be returned.")

    def forward_for_decision(self, feedback):
        # Action: forwardForDecision()
        if self.status == "UnderReview":
            self.status = "Approved" # (简化：在我们的流程中，FM复核后直接给AM)
            self.feedback_fm = feedback
        else:
            raise ValueError("Only requests UnderReview can be forwarded.")

    def reject(self, feedback):
        # Action: (Implied from Rejected state)
        if self.status in ["UnderReview", "Approved"]:
            self.status = "Rejected"
            self.feedback_am = feedback
        else:
            raise ValueError("Only requests UnderReview or Approved can be rejected.")
    
    def approve(self, feedback):
        # Action: (Implied from Approved state)
        if self.status == "Approved":
            self.status = "InProgress" # (我们用 InProgress 替代 "startExecution")
            self.feedback_am = feedback
        else:
            raise ValueError("Only Approved requests can be started.")
            
    def finalize(self):
        # Action: finalizeEvent()
        if self.status == "InProgress":
            self.status = "Closed"
        else:
            raise ValueError("Only InProgress requests can be finalized.")

# ====================================================================
# 工作流 2: Task and Plan
# ====================================================================

class Task:
    """
    Represents a Task for a sub-team.
    # 状态和转换基于 HW3 State Chart Diagram (Figure 7)
    """
    _id_counter = 1
    
    def __init__(self, event_request_id, title, description, assigned_to_team, created_by):
        self.id = Task._id_counter
        Task._id_counter += 1
        
        self.event_request_id = event_request_id
        self.title = title
        self.description = description
        self.assigned_to_team = assigned_to_team # e.g., "Decorations"
        self.created_by = created_by # e.g., "jack"
        
        self.status = "Created" #
        self.plan = None # Plan object will be linked here

    def assign(self):
        # Action: notifyNewTask()
        if self.status == "Created":
            self.status = "Assigned" #
        else:
            raise ValueError("Only Created tasks can be assigned.")

    def submit_plan(self, plan):
        # Action: submitPlan() & linkPlanToEvent()
        if self.status == "Assigned":
            self.plan = plan
            self.status = "Planned" # (我们跳过了InProgress)
        else:
            raise ValueError("Only Assigned tasks can receive a plan.")

    def mark_complete(self):
        # Action: markAsDone()
        if self.status == "Planned":
            self.status = "Completed" #
        else:
            raise ValueError("Only Planned tasks can be completed.")

class Plan:
    """
    Represents a plan submitted by a sub-team for a Task.
    # 基于 HW3 Figure 3 和 Figure 7
    """
    def __init__(self, details, resources_needed, budget_needs, submitted_by):
        self.details = details
        self.resources_needed = resources_needed
        self.budget_needs = budget_needs # e.g., 5000
        self.submitted_by = submitted_by
        self.timestamp = datetime.datetime.now()

# ====================================================================
# 工作流 3: Staffing Request
# ====================================================================

class StaffingRequest:
    """
    Represents a request for HR to recruit or outsource.
    # 状态和转换基于 HW3 State Chart Diagram (Figure 8)
    """
    _id_counter = 1
    
    def __init__(self, event_request_id, department, job_title, job_description, requested_by):
        self.id = StaffingRequest._id_counter
        StaffingRequest._id_counter += 1
        
        self.event_request_id = event_request_id
        self.department = department #
        self.job_title = job_title #
        self.job_description = job_description #
        self.requested_by = requested_by
        
        self.status = "Submitted" # (跳过 Draft)
        self.hr_decision = None # e.g., "Hiring" or "Outsourcing"
        self.hr_feedback = None

    def process(self, decision, feedback):
        # Action: evaluateRequest()
        if self.status == "Submitted":
            if decision not in ["Hiring", "Outsourcing", "Rejected"]:
                raise ValueError("Decision must be Hiring, Outsourcing, or Rejected.")
            
            self.hr_decision = decision
            self.hr_feedback = feedback
            if decision == "Rejected":
                self.status = "Rejected" #
            else:
                self.status = "Resolved" # (Hiring/Outsourcing 都算 Resolved)
        else:
            raise ValueError("Only Submitted requests can be processed.")

# ====================================================================
# 工作流 4: Financial Request
# ====================================================================

class FinancialRequest:
    """
    Represents a request for budget adjustment.
    # 基于 HW Business Case
    """
    _id_counter = 1

    def __init__(self, event_request_id, department, required_amount, reason, requested_by):
        self.id = FinancialRequest._id_counter
        FinancialRequest._id_counter += 1
        
        self.event_request_id = event_request_id
        self.department = department #
        self.required_amount = required_amount #
        self.reason = reason #
        self.requested_by = requested_by
        
        self.status = "Submitted"
        self.fm_feedback = None

    def approve(self, feedback):
        if self.status == "Submitted":
            self.status = "Approved"
            self.fm_feedback = feedback
        else:
            raise ValueError("Only Submitted requests can be approved.")

    def reject(self, feedback):
        if self.status == "Submitted":
            self.status = "Rejected"
            self.fm_feedback = feedback
        else:
            raise ValueError("Only Submitted requests can be rejected.")