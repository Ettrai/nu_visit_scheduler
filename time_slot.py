class TimeSlot:

    def __init__(self, id):
        self.id = id
        self.matched_id = -1

    def __lt__(self, other):
        return self.id < other.id


def id_to_time_window(id):

    if(id == 0):
        return "10.00 AM to 10.30 AM"

    if(id == 1):
        return "10.30 AM to 11.00 AM"

    if(id == 2):
        return "11.00 AM to 11.30 AM"

    if(id == 3):
        return "11.30 AM to 12.00 PM"