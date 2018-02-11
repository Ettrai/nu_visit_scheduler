import csv
import data as db
import student as st
import faculty as fc
import time_slot
import config

def print_list(data):

    for entry in data:
        print entry

def schedule():

    # Goes through faculty preferences first
    while(1):
        updated = False
        for f_entry in db.faculty_data:

            faculty = db.faculty_data[f_entry]

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
        for s_entry in db.student_data:

            student = db.student_data[s_entry]

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
st.load_student_list()
fc.load_faculty_list()

st.load_students_preferences()
fc.load_faculties_preferences()
fc.load_faculties_time_slots()



# for student in db.student_data:
#     print_student_data(db.student_data[student])
#     print

#
#
# # print
# # for entry in db.student_data:
# #     print_student_data(entry)
# #
# for entry in db.faculty_data:
#     print_faculty_data(db.faculty_data[entry])
#     print

schedule()

print "\t ##### FACULTY SCHEDULE #####"
print
print
for entry in db.faculty_data:
    fc.print_faculty_data(db.faculty_data[entry])
    print
print


print "\t ##### STUDENT SCHEDULE #####"
print
print
for entry in db.student_data:
    st.print_student_data(db.student_data[entry])
    print





