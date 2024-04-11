valid_courses = []
GradeID = "G4"
COURS_TAKE = {
            "a-mharic":["G4","G5","G6","G7","G8"],
            "m-oral":["G4","G5","G6"],
            "genral-science":["G7","G8"],
            "a-fanoromo":["G4","G5","G6","G7","G8"],
            "s-cience":["G4","G5","G6"],
            "m-aths":["G4","G5","G6","G7","G8"],
            "e-nglish":["G4","G5","G6","G7","G8"],
            "i-ct":["G4","G5","G6","G7","G8"],
            "c-te":["G7","G8"],
            "citizen-ship":["G7","G8"],
            "h-arari":["G4","G5","G6","G7","G8"],
            "social-studies":["G7","G8"]
        }
for key,item in COURS_TAKE.items():
    if GradeID in item:
        valid_courses.append(key)
print(valid_courses)

"""l = [[1, 3], [23, 1], [1, 0], [6, 0], [5, 3], [6, 0]]

d = {}
for i, value1 in enumerate(l):
    m = 0
    sublist = []
    for value2 in l:
        if value1[0] == value2[0]:
            m += 1
            sublist.append(value2)
    if m >= 2:
        d[i] = sublist

print(d)"""