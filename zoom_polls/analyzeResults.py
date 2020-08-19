import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--responses', '-r')
parser.add_argument('--answers', '-a')
parser.add_argument('--output', '-o')
args = parser.parse_args()

print("Reading responses", args.responses)
print("Checking against answers", args.answers)
print("Storing in output file", args.output)
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
        name = row[1]
        if name not in scores: scores[name] = 0
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
            scores[name] += points_answered
            if a == questions[q]: scores[name] += points_right

print(scores)

