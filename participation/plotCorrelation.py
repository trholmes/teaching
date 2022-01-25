# Script for plotting the correlation between different features

import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv
import glob

#grade_csv = glob.glob("221_Data/overall/2021*")[0]
#participation_csv = glob.glob("221_Data/overall/Participation Grade*")[0]
grade_csv = glob.glob("221_Data/final/2021*")[0]
participation_csv = glob.glob("221_Data/final/Participation Grade*")[0]

max_week = 12
n_header_cols = 5
n_participation_types = 5

def getFloat(cell):
    if cell=='': return 0.
    else: return float(cell)

grades = {}
with open(grade_csv, "r") as f:
    all_grades = csv.DictReader(f)
    for line in all_grades:
        if line["Student"] == "    Points Possible": continue
        if line["Student"] == "Student, Test": continue
        if line["Student"] == '': continue
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
        ave_openstax = 0
        ave_notes = 0
        for x in range(max_week):
            ave_oh      += getFloat(line[n_header_cols+n_participation_types*x+0])/max_week
            ave_zoom    += getFloat(line[n_header_cols+n_participation_types*x+1])/max_week
            ave_piazza  += getFloat(line[n_header_cols+n_participation_types*x+2])/max_week
            ave_openstax+= getFloat(line[n_header_cols+n_participation_types*x+3])/max_week
            ave_notes   += getFloat(line[n_header_cols+n_participation_types*x+4])/max_week
        participation[userid] = {"oh": ave_oh, "zoom": ave_zoom, "piazza": ave_piazza, "openstax": ave_openstax, "notes": ave_notes}

# Plot OH attendees vs other
def getAveGrades(condition):
    grade_arr = [0,0,0,0,0]
    n_students = 0
    for userid in grades:
        if eval(condition):
            n_students += 1
            grade_arr[0] += getFloat(grades[userid]["Assignments Current Score"])
            grade_arr[1] += getFloat(grades[userid]["Labs Current Score"])
            grade_arr[2] += getFloat(grades[userid]["Participation Current Score"])
            grade_arr[3] += getFloat(grades[userid]["Graded Exams Current Score"])
            grade_arr[4] += getFloat(grades[userid]["Current Score"])
    for i in range(len(grade_arr)):
        grade_arr[i] = grade_arr[i]/n_students
    print(condition, "Exam ave:", grade_arr[3])
    return grade_arr

def makePlotVsIndivParticipation(participation, minval, yes_str, no_str):
    fig,ax = plt.subplots()
    labels = ["Homeworks", "Labs", "Participation", "Exams", "Total"]
    yes_ohs = getAveGrades('participation[userid]["%s"] > %f'%(participation, minval))
    no_ohs = getAveGrades('participation[userid]["%s"] <= %f'%(participation, minval))
    plt.plot(range(len(yes_ohs)), yes_ohs, "o-", label=yes_str)
    plt.plot(range(len(no_ohs)), no_ohs, "o-", label=no_str)
    plt.ylabel('Average %')
    plt.xticks([0,1,2,3,4], labels)
    plt.ylim([40,150])
    plt.grid(alpha=0.5)
    plt.legend()
    fig.set_size_inches(6,2.5)
    fig.savefig('grade_vs_%s.png'%participation)

makePlotVsIndivParticipation("oh", 1, "Students Who Attend OHs", "Students Who Don't Attend OHs")
makePlotVsIndivParticipation("zoom", 10, "Students Who Do Clickers", "Students Who Don't Do Clickers")
makePlotVsIndivParticipation("piazza", 5, "Students Who Use Discussion", "Students Who Don't Use Discussion")
makePlotVsIndivParticipation("openstax", 4, "Students Who Don't Use OpenStax", "Students Who Don't Use OpenStax")
makePlotVsIndivParticipation("notes", 4, "Students Who Submit Notes", "Students Who Don't Submit Notes")

