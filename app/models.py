# 你们将在这里TDD你们的类
# 例如，基于 HW3 State Chart

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
        self.created_by = created_by #
        
        self.status = "Draft" # 初始状态

    def submit(self):
        """
        Action: submit()
        Transitions from Draft -> Submitted
        """
        if self.status == "Draft":
            self.status = "Submitted"
        else:
            raise Exception("Only Draft requests can be submitted.")
            
    def route_to_senior_officer(self):
        """
        Action: routeToSeniorOfficer(request)
        Transitions from Submitted -> UnderReview
        """
        if self.status == "Submitted":
            self.status = "UnderReview"
        else:
            raise Exception("Only Submitted requests can be routed.")

# ... (TDD将驱动你们在这里添加更多方法，如: forwardForDecision, startExecution 等) ...
# ... 例如: def forwardForDecision(self):
# ... 例如: def approve(self): self.status = "Approved"
# ... 例如: def reject(self): self.status = "Rejected"