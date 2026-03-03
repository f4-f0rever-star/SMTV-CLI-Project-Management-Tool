import json
import os
from app.user import User
from app.project import Project
from app.task import Task

class Storage:
    DATA_FILE = "data.json"

    @staticmethod
    def load_data():
        if not os.path.exists(Storage.DATA_FILE):
            return []
        
        try:
            with open(Storage.DATA_FILE, "r") as f:
                data = json.load(f)
                users = []

                for user_data in data:
                    current_user = User(user_data["name"], user_data["email"])
                
                    for project_data in user_data.get("projects", []):
                        new_project = Project(project_data["title"], project_data["description"], project_data["due_date"])

                        for task_data in project_data.get("tasks", []):
                            new_task = Task(task_data["title"], task_data["status"], task_data.get("assigned_to"))
                            new_project.tasks.append(new_task)

                        current_user.projects.append(new_project)

                    users.append(current_user)
            
                return users
        except(json.JSONDecodeError, KeyError, FileNotFoundError):
            return []
    
    @staticmethod
    def save_data(users):
        
        with open(Storage.DATA_FILE, "w") as f:
            json.dump([user.to_dict() for user in users], f, indent = 4)