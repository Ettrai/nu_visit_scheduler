import data as db
import time_slot
import csv
import config
import faculty as fc

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

def load_student_list():
    with open('data/students/list.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            db.student_list.append(row[0])

def load_students_preferences():
    with open('data/students/preferences.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            # Create new student object
            new_id = name_to_id(row[0])
            new_student = Student(new_id)
            # Populate preferences
            temp_slots = []
            for preference in row[1:]:
                temp_id = fc.name_to_id(preference)
                new_student.preferences.append(temp_id)

            for slot in range(config.num_time_slots):
                new_slot = time_slot.TimeSlot(slot)
                temp_slots.append(new_slot)
            new_student.time_slots = temp_slots

            # Store new student
            db.student_data[new_id] = new_student

def print_student_data(student):
    print "Student Name:", student.get_name()

    if(student.schedule):
        schedule = student.schedule
        schedule.sort()
        for index, entry in enumerate(schedule):
            print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.faculty_list[entry.matched_id]

    preferences = student.preferences
    for index, entry in enumerate(preferences):
        print "\tUnmatched preference:", db.faculty_list[entry], "->",len(db.faculty_data[entry].time_slots),"available slots"

    # print "\tTime Slots"
    # time_slots = student.time_slots
    # for entry in time_slots:
    #     print "\t\tAvailable", time_slot.id_to_time_window(entry.id)