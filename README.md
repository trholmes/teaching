# Teaching scripts

## Working with Zoom polls

Zoom polls can be made for each meeting, and the responses can be [exported](https://support.zoom.us/hc/en-us/articles/216378603) to a CSV.
You can import the questions from a CSV as well, which I've found is easiest to do via the Canvas Zoom interface.  I made scripts to take the 
responses and generate a template for the correct answers, then another script that scores participants based on responses.

How to run:
After you've downloaded your csv of responses, `pollFile.csv`, run 

```python zoom_polls/logAnswers.py -r pollFile.csv -a answerFile.json```

This will make a JSON file with all questions and all answers that were given in the class. You can delete all the
wrong answers to get a dictionary of all questions with correct answers. This can probably be done in a more streamlined way.
You might sometimes have to add the right answer in manually if no one answered it right.

Then when that file has been edited, you can run 

```python zoom_polls/analyzeResults.py -r pollFile.csv -a answerFile.json -o outputFile.csv -u usernames.txt```

which will give you a CSV file with scores that can be imported to Canvas. The `usernames.txt` file is just a text file with the usernames for your students (taken from an exported Canvas gradebook). 
