import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--participants', '-p')
parser.add_argument('--user', '-u')
parser.add_argument('--output', '-o')
args = parser.parse_args()

print("Getting participants", args.participants)
print("Storing in output file", args.output)
print("File for usernames", args.user)
print()

# Scoring options
points_for_showing = 5
scores = {}

#Name (Original Name),User Email,Join Time,Leave Time,Duration (Minutes)

with open(args.participants, newline='') as respfile:
    reader = csv.reader(respfile)
    for row in reader:
        if '(Original Name)' in row[0]: continue
        name = row[1].split("@")[0]
        if name not in scores:
            scores[name] = {
                    "User Name": row[0],
                    "User Email": row[1],
                    "User ID": name,
                    "Score": 0,}
        minutes = int(row[4])
        if minutes>15: scores[name]["Score"] = 5

# Compare to list of users
users = []
with open(args.user, 'r') as f:
    for line in f:
        users.append(line.strip("\n"))
print("Poll respondants not in database:")
for person in scores:
    if scores[person]["User ID"] not in users:
        print("\t%s\t%s\t%s"%(scores[person]["User ID"], scores[person]["User Name"], scores[person]["Score"]))

csv_columns = ["User Name", "User ID", "Score"]
with open(args.output, 'w') as csvfile:
    outstr = ""
    for col in csv_columns: outstr += "%s,"%col
    outstr += "\n"
    csvfile.write(outstr)
    for person in users:
        outstr = ""
        if person in scores:
            for col in csv_columns: outstr += "%s,"%scores[person][col]
        outstr += "\n"
        csvfile.write(outstr)




