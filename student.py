import data as db

class Student:
    def __init__(self, id):
        self.id = id
        self.preferences = []
        self.schedule = []
        self.time_slots = []


    def get_name(self):
        return id_to_name(self.id)

def id_to_name(id):
    return db.student_list[id]

def name_to_id(name):
    return db.student_list.index(name)

def id_to_student(id):

    for student in db.student_data:
        if student.id == id:
            return student
