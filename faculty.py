import data as db
import csv
import time_slot
import student as st

class Faculty:
    def __init__(self, id):
        self.id = id
        self.time_slots = []
        self.preferences = []
        self.schedule = []

    def get_name(self):
        return id_to_name(self.id)

def id_to_name(id):
    return db.faculty_list[id]

def name_to_id(name):
    return db.faculty_list.index(name)

def id_to_faculty(id):

    for faculty in db.faculty_data:
        if faculty.id == id:
            return faculty

def load_faculty_list():
    with open('data/faculties/list.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            db.faculty_list.append(row[0])

def load_faculties_preferences():
    with open('data/faculties/preferences.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            # Create new faculty object
            new_id = name_to_id(row[0])
            new_faculty = Faculty(new_id)
            # Populate preferences
            for preference in row[1:]:
                temp_id = st.name_to_id(preference)
                new_faculty.preferences.append(temp_id)
            # Store new faculty
            db.faculty_data[new_id] = new_faculty

def load_faculties_time_slots():
    with open('data/faculties/time_slots.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:

            id = name_to_id(row[0])

            temp_slots = []
            for slot in row[1:]:
                new_slot = time_slot.TimeSlot(int(slot))
                temp_slots.append(new_slot)
            temp_slots.sort()

            db.faculty_data[id].time_slots = temp_slots

def print_faculty_data(faculty):
    print "Faculty Name:", faculty.get_name()

    if(faculty.schedule):
        schedule = faculty.schedule
        for index, entry in enumerate(schedule):
            print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.student_list[entry.matched_id]

    time_slots = faculty.time_slots

    for entry in time_slots:
        print "\tAvailable", time_slot.id_to_time_window(entry.id)

    preferences = faculty.preferences
    for index, entry in enumerate(preferences):
        print "\tUnmatched preference:", db.student_list[entry], "->",len(db.student_data[entry].time_slots),"available slots"