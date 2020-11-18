# Script for plotting the correlation between different features

import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv

grade_csv = "221_Data/Midterm1.csv"

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

maxgrade = 17
nbins = 6
nlabels = 6

def getNormalizedGrades(condition):
    err_arr = []
    grade_arr = [0]*nbins
    n_students = 0
    for userid in grades:
        if eval(condition):
            n_students += 1
            grade = getFloat(grades[userid]["Midterm 1 (751377)"])
            grade_bin = int(grade/(maxgrade+1)*nbins)
            grade_arr[grade_bin] += 1
    for i in range(len(grade_arr)):
        err_arr.append(math.sqrt(grade_arr[i])/n_students)
        grade_arr[i] = grade_arr[i]/n_students
    return grade_arr, err_arr

fig,ax = plt.subplots()
labels = [str(i/(maxgrade+1)*nlabels) for i in range(nlabels)]
sec_22,sec_22_err           = getNormalizedGrades('grades[userid]["Section"] == "PHYS221 Section 022"')
not_sec_22, not_sec_22_err  = getNormalizedGrades('grades[userid]["Section"] != "PHYS221 Section 022"')

print(sec_22)
print(sec_22_err)
print(len(sec_22))
print(len(sec_22_err))

plt.plot(range(len(sec_22)), sec_22, "k", color="#000000")
plt.plot(range(len(not_sec_22)), not_sec_22, "k", color="#000000")
dw = [sec_22[i] - sec_22_err[i] for i in range(nbins)]
up = [sec_22[i] + sec_22_err[i] for i in range(nbins)]
plt.fill_between(range(nbins), dw, up, label="Students In Section 22", alpha=0.5)
dw = [not_sec_22[i] - not_sec_22_err[i] for i in range(nbins)]
up = [not_sec_22[i] + not_sec_22_err[i] for i in range(nbins)]
plt.fill_between(range(nbins), dw, up, label="Students Not In Section 22", alpha=0.5)
#plt.xticks([i for i in range(nlabels)], labels)
plt.legend()
plt.show()





