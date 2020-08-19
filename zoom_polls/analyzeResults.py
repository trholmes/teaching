import argparse

parser = argparse.ArgumentParser()
parser.add_argument('responses', metavar='r')
parser.add_argument('answers', metavar='a')
args = parser.parse_args()

print("Reading responses", args.responses)
print("Checking against answers", args.answers)





