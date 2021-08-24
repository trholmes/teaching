# Example script for running everything

PREFIX=M12

#python logAnswers.py -r 221_Data/${PREFIX}/${PREFIX}_PollReport.csv -a 221_Data/${PREFIX}/${PREFIX}_Answers.json

# Make sure to remove wrong answers from _Answers file now!

#python analyzeResults.py -r 221_Data/${PREFIX}/${PREFIX}_PollReport.csv -a 221_Data/${PREFIX}/${PREFIX}_Answers.json -o 221_Data/${PREFIX}/${PREFIX}_Grades.csv -u 221_Data/All_IDs.txt

# For office hours
#python getOH.py -p 221_Data/${PREFIX}/${PREFIX}_OHs.csv -o 221_Data/${PREFIX}/${PREFIX}_OHGrades.csv -u 221_Data/All_IDs.txt

# For OpenStax
python getOpenStax.py -g 221_Data/${PREFIX}/${PREFIX}_OpenStax/Full\ Class\ -\ %-Table\ 1.csv -o 221_Data/${PREFIX}/${PREFIX}_OSGrades.csv -u 221_Data/All_IDs.txt -m ${PREFIX}

