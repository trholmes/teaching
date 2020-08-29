# Example script for running everything

PREFIX=M1

#python logAnswers.py -r 221_Data/${PREFIX}_PollReport.csv -a 221_Data/${PREFIX}_Answers.json

# Make sure to remove wrong answers from _Answers file now!

python analyzeResults.py \
    -r 221_Data/${PREFIX}_PollReport.csv \
    -a 221_Data/${PREFIX}_Answers.json \
    -o 221_Data/${PREFIX}_Grades.csv \
    -u 221_Data/All_IDs.txt

