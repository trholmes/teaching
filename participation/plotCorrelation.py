# Script for plotting the correlation between different features

import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv

grade_csv = "221_Data/overall/2020-09-18T0807_Grades-PHYS221.csv"
participation_csv = "221_Data/overall/Participation Grade - Grade Entry.csv"

max_week = 3
n_header_cols = 5

def getFloat(cell):
    if cell=='': return 0.
    else: return float(cell)

grades = {}
with open(grade_csv, "r") as f:
    all_grades = csv.DictReader(f)
    for line in all_grades:
        if line["Student"] == "    Points Possible": continue
        if line["Student"] == "Student, Test": continue
        userid = line['SIS Login ID']
        grades[userid] = line

participation = {}
with open(participation_csv, "r") as f:
    all_participation = csv.reader(f)
    for i, line in enumerate(all_participation):
        if i<3: continue
        userid = line[3]
        ave_zoom = 0
        ave_oh = 0
        ave_piazza = 0
        for x in range(max_week):
            ave_oh      += getFloat(line[n_header_cols+3*x+0])/max_week
            ave_zoom    += getFloat(line[n_header_cols+3*x+1])/max_week
            ave_piazza  += getFloat(line[n_header_cols+3*x+2])/max_week
        participation[userid] = {"oh": ave_oh, "zoom": ave_zoom, "piazza": ave_piazza}

# Plot OH attendees vs other
def getAveGrades(condition):
    grade_arr = [0,0,0,0]
    n_students = 0
    for userid in grades:
        if eval(condition):
            n_students += 1
            grade_arr[0] += getFloat(grades[userid]["Assignments Current Score"])
            grade_arr[1] += getFloat(grades[userid]["Labs Current Score"])
            grade_arr[2] += getFloat(grades[userid]["Participation Current Score"])
            grade_arr[3] += getFloat(grades[userid]["Current Score"])
    for i in range(len(grade_arr)):
        grade_arr[i] = grade_arr[i]/n_students
    return grade_arr

fig,ax = plt.subplots()
labels = ["Homeworks", "Labs", "Participation", "Total"]
yes_ohs = getAveGrades('participation[userid]["oh"] > 0')
no_ohs = getAveGrades('participation[userid]["oh"] == 0')
plt.plot(range(len(yes_ohs)), yes_ohs, "o", label="Students Who Attend OHs")
plt.plot(range(len(no_ohs)), no_ohs, "o", label="Students Who Don't Attend OHs")
plt.xticks([0,1,2,3], labels)
plt.legend()
plt.show()

fig,ax = plt.subplots()
labels = ["Homeworks", "Labs", "Participation", "Total"]
yes_ohs = getAveGrades('participation[userid]["piazza"] >= 8')
no_ohs = getAveGrades('participation[userid]["piazza"] < 8')
plt.plot(range(len(yes_ohs)), yes_ohs, "o", label="Students With ≥ 8 Piazza Ave")
plt.plot(range(len(no_ohs)), no_ohs, "o", label="Students With < 8 Piazza Ave")
plt.xticks([0,1,2,3], labels)
plt.legend()
plt.show()





