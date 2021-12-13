import glob
import os
import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--dir', '-d')
parser.add_argument('--user', '-u')
parser.add_argument('--output', '-o')
parser.add_argument('--module', '-m')
args = parser.parse_args()
print(args.dir)

fname = glob.glob(os.path.join(args.dir, "Phys_221_*/All Students - %-Table 1.csv"))[0]

print("Module", args.module)
print("Getting grades from OpenStax", fname)
print("Storing in output file", args.output)
print("File for usernames", args.user)
print()

scores = {}

# Get positions we need to parse
student_id_col = 2
grades_start_row = 10
mod_num = int(args.module.strip("M"))
mod_name_col = 5+mod_num
mod_name_col = 6 # Actually it seems to insert them at the beginning...

#,,,Averages,,,Module 1 Additional Material,
#,,,,,,Due 1/26/2021,
#,,,Course Average*,Homework Averages,Reading Averages,Score,
#First Name,Last Name,Student ID,,,,,

with open(fname, newline='') as respfile:
    reader = csv.reader(respfile)

    for i, row in enumerate(reader):
        if i < grades_start_row:
            if row[3] == "Averages":
                mod_name_col = row.index("Module %d Additional Material"%mod_num)
                print("Found module in column", mod_name_col)
            continue
        if row[0] == "Class Average": break

        name = row[student_id_col]
        raw_score = row[mod_name_col]
        if raw_score == '': score = 0
        else: score = float(raw_score.strip("%"))*.1
        if name not in scores:
            scores[name] = score

# Compare to list of users
users = []
with open(args.user, newline='') as userfile:
    user_reader = csv.reader(userfile, delimiter='\t')
    for row in user_reader:
        users.append(row[3]) #Categorize by students' userids
print("Poll respondants not in database:")
for person in scores:
    if person not in users:
        print("\t%s\t%s"%(person, scores[person]))

csv_columns = ["User ID", "Score"]
with open(args.output, 'w') as csvfile:
    outstr = ""
    for col in csv_columns: outstr += "%s,"%col
    outstr += "\n"
    csvfile.write(outstr)
    for person in users:
        outstr = ""
        if person in scores:
            outstr += "%s,%s"%(person,scores[person])
        outstr += "\n"
        csvfile.write(outstr)




