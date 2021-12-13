import pandas as pd
import glob

def getGrade(number):
    lower_bounds = {
            0:   'F',
            60:  'D-',
            63:  'D',
            67:  'D+',
            70:  'C-',
            73:  'C',
            77:  'C+',
            80:  'B-',
            83:  'B',
            87:  'B+',
            90:  'A-',
            93:  'A',
    }
    lb = 0
    for b in lower_bounds:
        if b < number and b > lb:
            lb = b
    return lower_bounds[lb]

# Metadata
term_code = 202140
crns = {
        12: 41695,
        13: 41696,
        14: 41697,
        15: 41698,
        16: 47018,
        17: 41699,
        18: 41700,
        19: 41701,
        }

# Find name of template
template_name = glob.glob("221_Data/GradeEntry/*Template.xlsx")[0]
print("Template:", template_name)

# Find file with all grades
grades_name = glob.glob("221_Data/GradeEntry/*PHYS221.csv")[0]
print("Full grade file:", grades_name)

# Load both into dataframes
df_template = pd.read_excel(template_name)
df_grades = pd.read_csv(grades_name)
df_grades.dropna(subset = ['Section'], inplace=True)

#print(df_template)
#print(df_grades)

# Loop over sections to create final versions
sections = df_grades.Section.unique()

for s in sections:
    if "," in s: continue

    print("\tWorking on section:", s)
    section_no = int(s.split()[-1])
    section_grades = df_grades[df_grades.Section==s]
    output_grades = df_template.copy()
    output_grades.drop(output_grades.index, inplace=True)

    i = 0
    for index,entry in section_grades.iterrows():
        student_df = pd.DataFrame([[term_code, crns[section_no], entry["Student"], entry["ID"], "No", "No", "Physics", getGrade(float(entry["Final Score"])), '', '', '', '', "Cannot modify default date"]], columns = list(output_grades.columns), index = [i])
        output_grades = output_grades.append(student_df)
        i += 1

    #print(output_grades)
    output_grades.to_excel("221_Data/GradeEntry/full_grades_%d.xlsx"%section_no)


