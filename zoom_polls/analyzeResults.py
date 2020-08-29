import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--responses', '-r')
parser.add_argument('--answers', '-a')
parser.add_argument('--output', '-o')
parser.add_argument('--user', '-u')
args = parser.parse_args()

print("Reading responses", args.responses)
print("Checking against answers", args.answers)
print("Storing in output file", args.output)
print("File for usernames", args.user)
print()

# Scoring options
points_for_answering_all = 10
points_for_answering_all_right = 5

with open(args.answers, "r") as f:
    questions = json.load(f)

scores = {}

#,User Name,User Email,Submitted Date/Time, -> After this is question, answer, question, answer, etc
first_q = 4
total_questions = len(questions)
points_answered = 1.*points_for_answering_all/total_questions
points_right = 1.*points_for_answering_all_right/total_questions

with open(args.responses, newline='') as respfile:
    reader = csv.reader(respfile)
    for row in reader:
        if '#' in row[0]: continue
        entries = len(row)
        name = row[2].split("@")[0]
        if name not in scores:
            scores[name] = {
                    "User Name": row[1],
                    "User Email": row[2],
                    "User ID": row[2].split("@")[0],
                    "Score": 0,}
        n_questions = int((entries-first_q-1)/2)
        for x in range(n_questions):
            q_i = first_q+x*2
            q = row[q_i]
            a = row[q_i+1]
            if q not in questions:
                print("You've done something wrong: this question isn't in your answers file.")
                print(q)
                print("Exiting.")
                exit()
            scores[name]["Score"] += points_answered
            if a in questions[q]: scores[name]["Score"] += points_right

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




