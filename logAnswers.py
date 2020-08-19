import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--responses', '-r')
parser.add_argument('--answers', '-a')
args = parser.parse_args()

print("Reading responses", args.responses)
print("Making answer template", args.answers)
print()

questions = {}

#,User Name,User Email,Submitted Date/Time, -> After this is question, answer, question, answer, etc
first_q = 4

with open(args.responses, newline='') as respfile:
    reader = csv.reader(respfile)
    for row in reader:
        if '#' in row[0]: continue
        entries = len(row)
        n_questions = int((entries-first_q-1)/2)
        for x in range(n_questions):
            q_i = first_q+x*2
            q = row[q_i]
            a = row[q_i+1]
            if q not in questions: questions[q] = []
            if a not in questions[q]: questions[q].append(a)

with open(args.answers, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(questions)
