from enum import Enum
from datetime import datetime, timedelta
from dateutil.parser import parse
from collections import defaultdict
import random
import json
import sys

# Convert all time between two datetime values into a set of
# discrete datetimes marking the potential onset of a class
def slice_date_range(start_date, end_date):
    day_class_hours = [10, 14, 18]
    class_duration = timedelta(hours=3)
    ret = []
    base_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range((end_date - start_date).days + 1):
        for j in day_class_hours:
            candidate = base_date + timedelta(days=i, hours=j)
            #print("candidate", candidate.isoformat())
            if candidate >= start_date and candidate + class_duration <= end_date:
                #print("accepted")
                ret.append(candidate)
    return ret

def check_if_all_entries_exists_in_array(entries, array):
  for entry in entries:
    if entry != array:
      return False
  return True

class Instructor:
    def __init__(self, name, capabilities, availability):
        self.name = name
        self.caps = capabilities
        self.avail = []
        for a,b in availability:
            a = parse(a)
            b = parse(b)
            # print(a.isoformat(), b.isoformat())
            self.avail += slice_date_range(a,b)

# Load and merge classes & instructor & availabilities data -> create instructors
with open('instructors.json', 'r') as f:
  instructorData = json.load(f)
with open('availabilities.json', 'r') as f:
  availabilityData = json.load(f)
with open('classes.json', 'r') as f:
  classesData = json.load(f)
  classesNames = classesData.keys()
instructors = []
for name in instructorData:
    i = instructorData[name]
    invalid = False
    for c in i["capabilities"]:
        if c not in classesNames:
            invalid = c
    if invalid == False:
        instructors.append(Instructor(name, i["capabilities"], availabilityData[name]))
    else:
        sys.exit("ERROR! INVALID INSTRUCTOR CAPABILITIY! " + invalid + " for " + i["name"])

# Get all potential combinations of (instructor, date) and store in dict keyed by class
potential = defaultdict(list)
for c in classesData:
    for i in instructors:
        if c not in i.caps:
            continue
        for a in i.avail:
            potential[c].append((i, a))

# Shuffle for "fairness"
# TODO allow seed to be specified
for k in potential:
    random.shuffle(potential[k])

# Generate the schedule
schedule = []
for c in list(classesData):
    if len(potential[c]) == 0:
        continue
    schedule.append((c, *(potential[c][1 % len(potential[c])])))
    1 // len(potential[c])
schedule.sort(key=lambda v: v[2])

# Write to disk
output = []
for c in schedule:
    output.append({
        'name': c[0], 
        'description': classesData[c[0]]['description'],
        'instructor': c[1].name, 
        'time': c[2].isoformat()
    })
with open("schedule.json", "w") as f:
    json.dump({'schedule': output}, f, indent=4)