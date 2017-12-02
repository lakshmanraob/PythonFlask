import datetime

place_name = "lake pichola"
visit_time = datetime.datetime.now().strftime("%H:%M:%S")
print(visit_time)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def get_time(time):
    return datetime.time(int(datetime.datetime.strptime(time, "%H:%M:%S").strftime("%H")),
                         int(datetime.datetime.strptime(time, "%H:%M:%S").strftime("%M")),
                         int(datetime.datetime.strptime(time, "%H:%M:%S").strftime("%S")))


def get_start_end(place_name):
    startH = int(datetime.datetime.strptime(visit_details[place_name]["start"], "%H:%M").strftime("%H"))
    startM = int(datetime.datetime.strptime(visit_details[place_name]["start"], "%H:%M").strftime("%M"))

    endH = int(datetime.datetime.strptime(visit_details[place_name]["end"], "%H:%M").strftime("%H"))
    endM = int(datetime.datetime.strptime(visit_details[place_name]["end"], "%H:%M").strftime("%M"))

    return datetime.time(startH, startM, 0), datetime.time(endH, endM, 0)


visit_details = {
    "lake pichola": {
        "start": "9:00",
        "end": "18:00"
    },
    "city palace udaipur": {
        "start": "9:30",
        "end": "17:30"
    },
    "jag mandir": {
        "start": "10:00",
        "end": "18:00"
    },
    "fatesagar lake": {
        "start": "10:00",
        "end": "17:00"
    },
    "hawa mahal": {
        "start": "9:00",
        "end": "17:00"
    },
    "city palace jaipur": {
        "start": "9:30",
        "end": "17:00"
    },
    "amber fort": {
        "start": "8:00",
        "end": "17:30"
    },
    "nahargarh fort": {
        "start": "10:00",
        "end": "17:30"
    },
    "albert hall museum": {
        "start": "9:30",
        "end": "16:30"
    },
    "jaisalmer fort": {
        "start": "9:00",
        "end": "17:00"
    },
    "gadisar lake": {
        "start": "00:00",
        "end": "11:59"
    },
    "jain temples": {
        "start": "08:00",
        "end": "12:00"
    },
    "tazia tower and badal palace": {
        "start": "08:00",
        "end": "18:00"
    }
}

#missing desert safari and jagadish temple

print(datetime.datetime.strptime(visit_details[place_name]["start"], "%H:%M").strftime("%M"))

start, end = get_start_end("lake pichola")
print(time_in_range(start, end, get_time(visit_time)))



# if place_name.lower() in 'lake pichola':
#     start = datetime.time(9, 30, 0)
#     end = datetime.time(17, 30, 0)
#     if time_in_range(start, end, datetime.time)
