# Script to turn clicker responses to participation grades

import glob
import argparse
import csv
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dir', '-d')
parser.add_argument('--output', '-o')
parser.add_argument('--user', '-u')
parser.add_argument('--module', '-m')
args = parser.parse_args()

fname = glob.glob(os.path.join(args.dir, "2021-*"))[0]

print("Reading grades", fname)
print("Storing in output file", args.output)
print("File for usernames", args.user)
print()

# Scoring options
points_cap= 5

scores = {}
users = []

with open(args.user, newline='') as userfile:
    user_reader = csv.reader(userfile, delimiter='\t')
    for row in user_reader:
        users.append(row[3]) #Categorize by students' userids

# Gather scores
with open(fname, newline='') as respfile:
    res_reader = csv.reader(respfile)
    col_num = -1
    for row in res_reader:
        if row[0] == 'Student':
            col_name = '%s Notes'%args.module
            for i, val in enumerate(row):
                if col_name in val:
                    col_num = i
                    print("Found assignment in column", i)
            continue
        if 'Points Possible' in row[0]: continue

        name = row[3]
        score = float(row[col_num])
        scores[name] = score

# Compare to list of users
print("Poll respondants not in database:")
for person in scores:
    if person not in users:
        print("\t%s\t%.2f"%(person, scores[person]))

csv_columns = ["User Name", "Score"]
with open(args.output, 'w') as csvfile:
    outstr = ""
    for col in csv_columns: outstr += "%s,"%col
    outstr += "\n"
    csvfile.write(outstr)
    for person in users:
        outstr = ""
        if person in scores:
            outstr += "%s,"%person
            outstr += "%f"%scores[person]
        outstr += "\n"
        csvfile.write(outstr)

