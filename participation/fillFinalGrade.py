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

# Find name of template
template_names = glob.glob("221_Data/GradeEntry/*Template.xlsx")

# Find file with all grades
grades_name = glob.glob("221_Data/GradeEntry/*PHYS221.csv")[0]
print("Full grade file:", grades_name)

# Load into dataframes
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
    template_name = [name for name in template_names if "%03d_Template"%section_no in name][0]
    df_template = pd.read_excel(template_name, dtype={'Student ID': str})

    section_grades = df_grades[df_grades.Section==s]
    for index,entry in section_grades.iterrows():
        name = entry["Student"]
        parsed_name = name.split(",")[1].strip()+" "+name.split(",")[0]
        #print(parsed_name)
        temp_index = df_template[df_template["Full Name"]==parsed_name].index.values
        if len(temp_index)==0:
            temp_index = df_template[df_template["Full Name"].str.endswith(name.split(",")[0].strip())].index.values
        if len(temp_index) != 1:
            print("Problem with grade for", parsed_name, "found", len(temp_index), "names")
        df_template.at[temp_index, 'Final Grade'] = getGrade(float(entry["Final Score"]))
        #df_template.at[temp_index, 'Student ID'] = "%09d"%df_template[temp_index,'Student ID']
        #print(temp_index)

    #print(df_template)
    df_template.to_excel("221_Data/GradeEntry/full_grades_%d.xlsx"%section_no)


