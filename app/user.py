class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []

    def to_dict(self):
        return {
            "name": self.name, 
            "email": self.email, 
            "projects": [project.to_dict() for project in self.projects]
        }

class Admin(User):
    def __init__(self, name, email):
        super().__init__(name, email)
        

    
    