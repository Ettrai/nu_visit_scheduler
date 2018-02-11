import data as db

class Faculty:
    def __init__(self, id):
        self.id = id
        self.time_slots = []
        self.preferences = []
        self.schedule = []

    def get_name(self):
        return id_to_name(self.id)

    def init_time_slots(self, time_slots):
        self.time_slots = time_slots

def id_to_name(id):
    return db.faculty_list[id]

def name_to_id(name):
    return db.faculty_list.index(name)

def id_to_faculty(id):

    for faculty in db.faculty_data:
        if faculty.id == id:
            return faculty

