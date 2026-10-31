class Course:
    def __init__(self, id, title, instructor, description):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.description = description

    def to_dict(self):
        return {"id": self.id, "title": self.title, "instructor": self.instructor, "description": self.description}