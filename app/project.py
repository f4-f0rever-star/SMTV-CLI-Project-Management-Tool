class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []

    def to_dict(self):
        return {"title": self.title, "description": self.description, "due_date": self.due_date, "tasks": [task.to_dict() for task in self.tasks]}