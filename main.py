import csv
import data as db
import student as st
import faculty as fc
import time_slot
import config
import copy

def load_faculty_list():
    with open('data/faculties/list.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            db.faculty_list.append(row[0])

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
            new_id = st.name_to_id(row[0])
            new_student = st.Student(new_id)
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
            db.student_data.append(new_student)

def load_faculties_preferences():
    with open('data/faculties/preferences.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            # Create new faculty object
            new_id = fc.name_to_id(row[0])

            print row[0], new_id

            new_faculty = fc.Faculty(new_id)
            # Populate preferences
            for preference in row[1:]:
                temp_id = st.name_to_id(preference)
                new_faculty.preferences.append(temp_id)
            # Store new faculty
            db.faculty_data.append(new_faculty)

def load_faculties_time_slots():
    with open('data/faculties/time_slots.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:

            id = fc.name_to_id(row[0])
            # print row[0], int(id)
            temp_slots = []
            for slot in row[1:]:
                new_slot = time_slot.TimeSlot(int(slot))
                temp_slots.append(new_slot)

            # for slot in temp_slots:
            #     print slot.id
            #
            # for i in temp_slots:
            #     print i.id

            temp_slots.sort()
            # print
            # for i in temp_slots:
            #     print i.id
            # print

            db.faculty_data[id].time_slots = copy.deepcopy(temp_slots)
            # print "Primo", db.faculty_data[id].time_slots[0].id




def print_student_data(student):
    print "Student Name:", student.get_name()

    if(student.schedule):
        schedule = student.schedule
        for index, entry in enumerate(schedule):
            print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.faculty_list[entry.matched_id]

    print "\tTime Slots"
    time_slots = student.time_slots
    for entry in time_slots:
        print "\tAvailable", time_slot.id_to_time_window(entry.id)

    preferences = student.preferences
    for index, entry in enumerate(preferences):
        print "\tPreference", index+1,"-", db.faculty_list[entry]

def print_faculty_data(faculty):
    print "Faculty Name:", faculty.get_name()

    # if(faculty.schedule):
    #     schedule = faculty.schedule
    #     for index, entry in enumerate(schedule):
    #         print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.student_list[entry.matched_id]

    time_slots = faculty.time_slots

    print time_slots[0].id

    for entry in time_slots:
        print "\tAvailable", time_slot.id_to_time_window(entry.id)

    preferences = faculty.preferences
    for index, entry in enumerate(preferences):
        print "\tPreference", index+1,"-", db.student_list[entry]
        print "\t\tAvailable slots:", len(db.student_data[entry].time_slots)

def print_student_schedule(student):
    print "Student Name:", student.get_name()

    if(student.schedule):
        schedule = student.schedule
        for index, entry in enumerate(schedule):
            print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.faculty_list[entry.matched_id]

    else:
        print "\tThis student has no schedule"

def print_faculty_schedule(faculty):
    print "Faculty Name:", faculty.get_name()

    if(faculty.schedule):
        schedule = faculty.schedule
        for index, entry in enumerate(schedule):
            print "\tScheduled", time_slot.id_to_time_window(entry.id), "with", db.student_list[entry.matched_id]
        print

    else:
        print "This faculty has no schedule"


def print_list(data):

    for entry in data:
        print entry

def schedule():

    # Goes through faculty preferences first
    while(1):
        updated = False
        for faculty in db.faculty_data:

            if(faculty.preferences and len(faculty.time_slots)):

                faculty_id = faculty.id
                student_id = faculty.preferences[0]

                student = db.student_data[student_id]

                force_match = False
                if(faculty_id not in student.preferences):

                    if(config.force_faculty_preference):
                        force_match = True

                    else:
                        continue

                f_time_slots = faculty.time_slots
                s_time_slots = student.time_slots

                matched = False
                for slot1 in f_time_slots:
                    for slot2 in s_time_slots:

                        if slot1.id == slot2.id:

                            matched = True
                            updated = True

                            slot1.matched_id = student_id
                            slot2.matched_id = faculty_id

                            faculty.schedule.append(slot1)
                            faculty.time_slots.remove(slot1)

                            student.schedule.append(slot2)
                            student.time_slots.remove(slot2)

                            faculty.preferences.remove(student_id)

                            if(force_match):
                                break

                            student.preferences.remove(faculty_id)

                            break

                    if(matched == True):
                        break

        if(not updated):
            break

    # Goes through student preferences
    while(1):
        updated = False
        for student in db.student_data:

            if(student.preferences and len(student.time_slots)):

                student_id = student.id
                faculty_id = student.preferences[0]

                faculty = db.faculty_data[faculty_id]

                f_time_slots = faculty.time_slots
                s_time_slots = student.time_slots

                matched = False
                for slot1 in f_time_slots:
                    for slot2 in s_time_slots:

                        if slot1.id == slot2.id:

                            matched = True
                            updated = True

                            slot1.matched_id = student_id
                            slot2.matched_id = faculty_id

                            faculty.schedule.append(slot1)
                            faculty.time_slots.remove(slot1)

                            student.schedule.append(slot2)
                            student.time_slots.remove(slot2)

                            student.preferences.remove(faculty_id)

                            break

                    if(matched == True):
                        break

        if(not updated):
            break





print

# Loading Data
load_faculty_list()
load_student_list()

load_students_preferences()

load_faculties_preferences()
load_faculties_time_slots()

# print
# for entry in db.student_data:
#     print_student_data(entry)
#
for entry in db.faculty_data:
    print_faculty_data(entry)
    print

# schedule()

# print "\t ##### FACULTY SCHEDULE #####"
# print
# print
# for entry in db.faculty_data:
#     print_faculty_data(entry)
#     print
# print
#
# # temp = faculty.id_to_faculty(0)
# # print_faculty_schedule(temp)
#
# #
# # for entry in db.student_data:
# #     print_student_data(entry)
#
# print "\t ##### STUDENT SCHEDULE #####"
# print
# print
# for entry in db.student_data:
#     print_student_data(entry)
#     print





