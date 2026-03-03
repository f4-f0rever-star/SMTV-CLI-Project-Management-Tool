class Task:
    def __init__(self, title, status = "Pending", assigned_to = None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def mark_done(self):
        self.status = "Done"

    def to_dict(self):
        return {"title": self.title, "status": self.status, "assigned_to": self.assigned_to}