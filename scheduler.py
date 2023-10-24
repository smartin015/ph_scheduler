# Brute-force schedule creation 

from enum import Enum
import random
from datetime import datetime, timedelta
from collections import defaultdict

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

class Instructor:
    def __init__(self, name, capabilities, availability):
        self.name = name
        self.caps = capabilities
        self.avail = []
        for a,b in availability:
            a = datetime.strptime(a, '%Y-%m-%d %H')
            b = datetime.strptime(b, '%Y-%m-%d %H')
            print(a.isoformat(), b.isoformat())
            self.avail += slice_date_range(a,b)

C = Enum('Class', ['CNCPlasma', 'GeneralWood', 'CNCRouter', 'MetalFlowers'])
instructors = [Instructor(n, c, a) for n, c, a in [
    ("Scott", 
        (C.CNCPlasma, C.CNCRouter), 
        (("2023-09-22 09", "2023-09-22 18"),
         ("2023-09-24 09", "2023-09-26 18"),
        )
    ),
    ("Nolan",
        (C.GeneralWood, C.CNCRouter),
        (("2023-09-22 09", "2023-09-24 18"),)
    ),
    ("Karen",
        (C.CNCPlasma, C.MetalFlowers),
        (("2023-09-24 00", "2023-09-26 18"),)
        )
    ]]

# Get all potential combinations of (instructor, date) and store in dict keyed by class
potential = defaultdict(list)
for c in C:
    for i in instructors:
        if c not in i.caps:
            continue
        for a in i.avail:
            potential[c].append((i, a))

# Shuffle for "fairness"
# TODO allow seed to be specified
for k in potential:
    random.shuffle(potential[k])

# Construct candidate schedules, using i to try all permutations of <class, instructor, date>
for i in range(5):
    candidate = []
    ci = i
    for c in list(C):
        if len(potential[c]) == 0:
            continue
        candidate.append((c, *(potential[c][ci % len(potential[c])])))
        ci // len(potential[c])

    candidate.sort(key=lambda v: v[2])
    print([(c[0].name, c[1].name, c[2].isoformat()) for c in candidate])
    
