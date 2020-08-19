# Teaching scripts

## Working with Zoom polls

Zoom polls can be made for each meeting, and the responses can be [https://support.zoom.us/hc/en-us/articles/216378603][exported] to a CSV.
So far I haven't figured out how to import them from a CSV, and anyway making them in the GUI is kind of nice. I made scripts to take the 
responses and generate a template for the correct answers, then another script that scores participants based on responses.

How to run:
After you've downloaded your csv of responses, `pollFile.csv`, run 

```python zoom_polls/logAnswers.py -r pollFile.csv -a answerFile.json```

This will make a JSON file with all questions and all answers that were given in the class. You can delete all the
wrong answers to get a dictionary of all questions with correct answers. This can probably be done in a more streamlined way.
You might sometimes have to add the right answer in manually if no one answered it right.

Then when that file has been edited, you can run 

```python zoom_polls/analyzeResults.py -r pollFile.csv -a answerFile.json -o outputFile.json```

which will give you a CSV file with scores that can be imported to Canvas (work in progress).
