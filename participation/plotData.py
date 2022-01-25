import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

### HELPER FUNCTIONS ###

    # Useful question numbers
    # 53 = race/ethnicity, 54 = gender, 58 = non-traditional students
    # 2 = transfers, 3 = year

# Set up simplified bins
simplified_bins = {
}

# Get bins for this hist
def getBins(resps, n_q, simplified=True):

    vals = np.array(responses[questions[n_q]])

    # Avoid issue with null responses
    cleaned_vals = vals[~pd.isnull(vals)]
    unique_vals = np.unique(cleaned_vals)
    if len(vals) != len(cleaned_vals):
        unique_vals = np.append(unique_vals, "No Response")

    # Option to use hardcoded combinations
    if simplified and n_q in simplified_bins:
        simp_vals = np.array(list(simplified_bins[n_q].keys()))
        if len(vals) != len(cleaned_vals):
            if "No Response" not in simplified_bins[n_q]:
                simp_vals = np.append(simp_vals, "No Response")
                simplified_bins[n_q]["No Response"] = ["No Response"]
        return simp_vals

    # Otherwise return unique list
    return unique_vals

# Simple poisson error
def getErr(arr):
    err_arr = []
    for entry in arr:
        err_arr.append(math.sqrt(entry))
    return err_arr

# Get a title and split it when appropriate
def getSplitString(s, max_words = 9):

    # Clean up super long titles
    if s.startswith("To what extent"):
        s = s.split('"')[1]

    n_words = len(s.split())
    n_breaks = int(n_words/max_words)
    if n_words <= max_words: return s

    title = ""
    br = 0
    for br in range(n_breaks):
        title += " ".join(s.split()[br*max_words:(br+1)*max_words])
        title += "\n"
    title += " ".join(s.split()[(br+1)*max_words:])
    return title

def getBinLabels(bins, max_words = 5):
    mod_bins = []
    for b in bins:
        if not type(b)==str:
            mod_bins.append(b)
        else:
            mod_bins.append(getSplitString(b, max_words))
    return mod_bins


# Get a histogram and its errors for a given question and selection
def getHistAndErr(resps, n_q, bins, sel="True", normalize=True, simplified=True):

    vals = np.array(responses[questions[n_q]])

    n_tot = 0
    bin_vals = [0]*len(bins)
    for j, val in enumerate(vals):
        if eval(sel):
            comp_val = val

            # Deal with null values
            if pd.isnull(val):
                comp_val = "No Response"
            elif "No Response" in bins and not (simplified and (n_q in simplified_bins)):
                comp_val = str(val)

            # Option to use simplified categories
            if simplified and n_q in simplified_bins:
                for k in simplified_bins[n_q]:
                    if comp_val in simplified_bins[n_q][k]:
                        comp_val = k
                        break

            i = np.where(bins == comp_val)[0][0]
            bin_vals[i] += 1
            n_tot += 1

    #if n_tot == 0:
    #    return [0], [0]

    bin_errs = getErr(bin_vals)

    if normalize:
        if n_tot > 0:
            for j in range(len(bin_vals)):
                    bin_vals[j] = bin_vals[j]/n_tot
                    bin_errs[j] = bin_errs[j]/n_tot

    return bin_vals, bin_errs

# Get mean value of distribution -- only valid for 1-5 distributions
def getMean(data, nprofs=False):

    val_index = [1, 2, 3, 4, 5]
    if nprofs: val_index = [0, 1, 2, 3, 4, 5]
    vals = data[:len(val_index)] # Strip off "no response"
    count = 0
    total = 0
    for i, v in enumerate(vals):
        count += v
        total += (val_index[i])*v
    if count>0: return total/count
    return -1

# Make a plot comparing response values for different selections
def plotData(resps, n_q, sels={"all":"True"}, app="", normalize=True, pie=False, simplified=True):

    bins = getBins(resps, n_q, simplified=simplified)
    data = {}
    for sel in sels:
        data[sel] = {}
        data[sel]["bin_vals"], data[sel]["bin_errs"] = getHistAndErr(resps, n_q, bins, sels[sel], normalize, simplified=simplified)

    maxxlabel = 0
    for x in bins: maxxlabel = max(len(str(x)), maxxlabel)

    # Figure out canvas size
    xsize = 5
    ysize = 5
    if maxxlabel > 30:
        xsize = 7
        ysize = 7
    if len(bins)>6:
        xsize = 9

    # Make plot
    fig, axs = plt.subplots(1, 1, figsize=(xsize,ysize))

    if pie:
        if len(sels) != 1:
            print("Cannot make pie chart for multiple selections yet.")
            return
        for sel in sels:
            #axs.pie(data[sel]["bin_vals"], explode=explode, labels=getBinLabels(bins), autopct='%1.1f%%', shadow=True, startangle=90)
            patches, texts, autotexts = axs.pie(data[sel]["bin_vals"], labels=getBinLabels(bins, 2), autopct='%1.1f%%', textprops={'fontsize': 12})
            axs.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            axs.margins(0.5)
            for autotext in autotexts:
                autotext.set_color('white')
            axs.set_title(getSplitString(questions[n_q]), fontsize=10)
            #plt.tight_layout()
            plt.savefig("plots/q_%d%s_pie.png"%(n_q, app))
        return

    for sel in sels:
        if showMean(n_q):
            axs.errorbar(range(len(bins)), data[sel]["bin_vals"], yerr=data[sel]["bin_errs"], label="%s (mean: %.2f)"%(sel, getMean(data[sel]["bin_vals"], nprofs=(n_q in [16, 17, 18, 19]))), marker="o")
        else: axs.errorbar(range(len(bins)), data[sel]["bin_vals"], yerr=data[sel]["bin_errs"], label=sel, marker="o")
    plt.xticks(range(len(bins)), getBinLabels(bins))
    axs.margins(0.2)
    plt.ylim(bottom=0)
    if normalize: plt.ylabel("Fraction in Group")
    else: plt.ylabel("Number of Respondents")
    #if n_q in [20, 21] + list(range(23,36)) + list(range(38,52)):
    #    for i, sel in enumerate(sels):
    #        plt.text(0.02, 0.9-0.1*i, "%s: %.2f"%(sel, getMean(data[sel]["bin_vals"])), transform=axs.transAxes)
    if len(questions[n_q].split())>30:
        plt.subplots_adjust(top=(1-len(questions[n_q].split())*0.005))
    if False: # maxxlabel > 15 and maxxlabel <= 30:
        plt.xticks(rotation=10)
        axs.set_xticklabels(getBinLabels(bins), ha='right')
        plt.subplots_adjust(bottom=maxxlabel*0.007)
    if maxxlabel > 15:
        plt.xticks(rotation=60)
        axs.set_xticklabels(getBinLabels(bins), ha='right')
        plt.subplots_adjust(bottom=min(0.4,maxxlabel*0.03))
    axs.set_title(getSplitString(questions[n_q]), fontsize=10)
    if len(sels)>1: plt.legend(loc='best', numpoints=1, framealpha=1) #, bbox_to_anchor=(0.5, 1.5))
    else:
        if showMean(n_q): plt.text(0.75, 0.85, "mean: %.2f"%(getMean(data[sel]["bin_vals"], nprofs=(n_q in [16, 17, 18, 19]))), transform = axs.transAxes)
    plt.savefig("plots/q_%d%s.png"%(n_q, app))

    return

def showMean(n_q):
    if n_q in [16, 17, 18, 19, 20, 21] + list(range(23,36)) + list(range(38,52)): return True
    return False

def getAllSelections(respsonses, n_q, simplified=True):
    selections = {}
    if simplified and n_q in simplified_bins:
        for k in simplified_bins[n_q]:
            selections[k] = "responses[questions[%d]][j] in simplified_bins[%d]['%s']"%(n_q, n_q, k)
        return selections

    values = getBins(respsonses, n_q)
    for v in values:
        if type(v)==np.int64: # Value is an int
            selections[v] = "responses[questions[%d]][j] == %s"%(n_q, v)
        else:
            selections[v] = "responses[questions[%d]][j] == '%s'"%(n_q, v)
    return selections

#resp_file = "data/Physics_Undergrad_Survey (Responses) - Form Responses 1.csv"
resp_file = "221_Data/221 Mid-term Poll (Responses) - Form Responses 1.csv"
questions = ['Timestamp','How are you doing in this class?','About how many hours a week are you spending on the class (including in-class time)?',
        'How are you finding the material? ','Have you taken a class that covered physics in some form before?',
        'What is the MOST useful thing for your understanding of the material?','What is the SECOND MOST useful thing for your understanding of the material?',
        'Would you like to have more time to discuss problems with your peers during Tuesday class?','Can you explain why or why not?',
        'If we started doing breakout sessions, how many people would you want in a group?','How useful do you find qualitative clicker polls about concepts?',
        'How useful do you find clicker polls in which you have to calculate an answer?','How do you feel about the independent learning component of this course?',
        'Do you attend office hours?','Do you use the discussion forum?','Any comments on how the discussion forum could be made into a more useful resource?',
        'Do you like having participation as a significant component of your grade?',"Anything else you'd like to say about the participation grade?",
        'Do you have an in-person lab section?',"The week of the midterm, I'll do a review class. Which topics would you MOST like covered?",
        "The week of the midterm, I'll do a review class. Which topics would you like covered SECOND MOST?",'How are you doing overall this semester?',
        'Any other comments?',"How do you feel about how much content is covered in Tuesday classes (keeping in mind that the overall content you're responsible for can't be changed)?",
        'How has the return to in-person classes has been for you so far?','How comfortable are you reaching out to your TA with questions?',
        'How comfortable are you reaching out to me with questions?','Any other comments on the structure of the Tuesday class?']

# Quickly get list of enumerated questions
#for i, q in enumerate(questions):
#    print(i, q)

with open(resp_file, newline='') as csvfile:
    responses = pd.read_csv(csvfile)

    #print(getBins(responses,55))
    #exit()

    # Useful question numbers

    #plotData(responses, 16, getAllSelections(responses, 54), app="_genders")

    for x in range(1, 28):

        plotData(responses, x, {"all":"True"}, app="_allspec", normalize=False, pie=True, simplified=False)
        plotData(responses, x, getAllSelections(responses, 2), app="_time")
        continue

