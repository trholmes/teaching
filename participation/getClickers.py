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
args = parser.parse_args()

fname = glob.glob(os.path.join(args.dir, "Module *"))[0]

print("Reading responses", fname)
print("Storing in output file", args.output)
print("File for usernames", args.user)
print()

# Scoring options
points_cap= 15

scores = {}
users = []

with open(args.user, newline='') as userfile:
    user_reader = csv.reader(userfile, delimiter='\t')
    for row in user_reader:
        users.append(row[0]) #Categorize by students' full names

# Gather scores
with open(fname, newline='') as respfile:
    res_reader = csv.reader(respfile)
    for row in res_reader:
        if row[0] == 'Device ID': continue
        name = row[1]+", "+row[2]
        points = float(row[4])
        tot_points = float(row[5])
        score = points_cap*points/tot_points
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

