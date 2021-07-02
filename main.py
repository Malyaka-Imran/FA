import pandas as pd
import numpy as np

from repeats import repeats
from score import score
#from factor_score import factor_analysis
from clean import clean
from match import match
from merge import merge
from id_gen import id_gen
import pandas as pd

'''
This is the new (Summer 2019) implementation of scoring, matching, and merging
'''
year = "18"
season = "S"
mergeName = 'QuaRCSLt2_merged.csv'
PREdata = 'QLt2_PRE.csv'
PSTdata = 'QLt3_POST.csv'
stu_DB_name, instr_DB_name = "Student_ID_Database.csv", "Instr_ID_Database.csv"

# Score PRE and PST data
# print("Scoring...")
PREdata = score(PREdata, 'PRE', year, season, 'answ.csv', PREdata[:-4])
PSTdata = score(PSTdata, 'PST', year, season, 'answ.csv', PSTdata[:-4])
#print(PREdata['PRE' + '_COMPFLAG'])
#print(PSTdata['PST' + '_COMPFLAG'])

# Calculating Factor Scores
#PREdata, PSTdata = factor_analysis(PREdata,'PRE', year, season), factor_analysis(PSTdata, 'PST', year, season)


# Clean PRE and PST
# PREdata, PSTdata = PREdata[:-4] + "_scored.csv", PSTdata[:-4] + "_scored.csv"
print("Cleaning...")
PREdata, PSTdata = clean(PREdata, 'PRE'), clean(PSTdata, 'PST')

# Generate IDs for PRE and PST
# PREdata, PSTdata = PREdata[:-4] + "_cleaned.csv", PSTdata[:-4] + "_cleaned.csv"
print("Generating student and instructor IDs...")
PREdata = id_gen(PREdata, 'PRE', year, season, stu_DB_name, instr_DB_name)
PSTdata = id_gen(PSTdata, 'PST', year, season, stu_DB_name, instr_DB_name)

# Split Repeats
print("Splitting...")
PREdata, PSTdata = repeats(PREdata, 'PRE'), repeats(PSTdata, 'PST')

# Match
# PREdata, PSTdata = pd.read_csv(PREdata[:-4] + "_id.csv"), pd.read_csv(PSTdata[:-4] + "_id.csv")
print("Matching...")
PRE_not_matched, PST_not_matched, pairs, instructor_change = match(PREdata, PSTdata)

# Merge
print("Merging...")
mergedData = merge(PRE_not_matched, PST_not_matched, PREdata, PSTdata, pairs)
mergedData.to_csv(mergeName, encoding='utf-8', index = False)
print("Merged dataset saved to {0}".format(mergeName))