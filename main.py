import pandas as pd
import numpy as np

def run():
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
  year = "21"
  season = "S"
  mergeName = 'QuaRCSLt2_'+season+year+'_merged.csv'
  PREdata = "QLt2_PRE.csv"
  PSTdata = "QLt2_POST.csv"
  stu_DB_name, instr_DB_name = "Student_ID_Database.csv", "Instr_ID_Database.csv"

  # Score PRE and PST data
  print("Scoring...")
  PREdata = score(PREdata, 'PRE', year, season, 'answ.csv', PREdata[:-4])
  PSTdata = score(PSTdata, 'PST', year, season, 'answ.csv', PSTdata[:-4])
  #print(PREdata['PRE' + '_COMPFLAG'])
  #print(PSTdata['PST' + '_COMPFLAG'])
  print("Scoring done")
  print("------------------------------------------------------")
  # Calculating Factor Scores
  # PREdata, PSTdata = factor_analysis(PREdata,'PRE', year, season), factor_analysis(PSTdata, 'PST', year, season)

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

  #PREdata.to_csv("PRE_processed.csv", encoding='utf-8', index=False)
  #PSTdata.to_csv("POST_processed.csv", encoding='utf-8', index=False)
  #print(pairs)
  # Merge
  print("Merging...")
  mergedData = merge(PRE_not_matched, PST_not_matched, PREdata, PSTdata, pairs)
  mergedData.to_csv(mergeName, encoding='utf-8', index = False)
  print("Merged dataset saved to {0}".format(mergeName))


def legacy_run():
  from score import score
  from legacy import only_complete, instructors_list, comments_fill, standardize, repeating_names
  from legacy import public_data_anonym, anonym_adder
  from legacy import merger, public_merged
  from legacy import match, match_refine

  '''
  This is the legacy implementation of scoring, matching, and merging
  '''

  PREdata = 'QuaRCSLt2_S18_PRE.csv'
  PSTdata = 'QuaRCSLt2_S18_POST.csv'

  test_administered_date = 'Fa18'

  # Score PRE and PST
  score(PREdata, 'PRE', 'answ.csv', PREdata[:-4])
  score(PSTdata, 'PST', 'answ.csv', PSTdata[:-4])
  

  # Clean
  data_PRE = pd.read_csv('QuaRCSLt2_S18_PRE_scored.csv', encoding = 'utf-8')
  data_POST = pd.read_csv('QuaRCSLt2_S18_POST_scored.csv', encoding = 'utf-8')

  data_POST, data_POST_dropped = only_complete(data_POST, 'PST')
  data_POST_dropped = instructors_list(data_POST_dropped, 'PST')
  data_POST = instructors_list(data_POST, 'PST')
  print("Edited PST columns")

  data_PRE, data_PRE_dropped = only_complete(data_PRE, 'PRE')
  data_PRE_dropped = instructors_list(data_PRE_dropped, 'PRE')
  data_PRE = instructors_list(data_PRE, 'PRE')
  print("Edited PRE columns")

  # Matching
  prelim_no_matches_pre, prelim_no_matches_post, prelim_pairs, prelim_instructor_change = match(data_PRE, data_POST)
  print("Matched")

  retakes_pre, retakes_post = repeating_names(data_PRE), repeating_names(data_POST)
  print("Found retakes")

  no_matches_pre, no_matches_post, pairs, instructor_change = match_refine(prelim_no_matches_pre, prelim_no_matches_post, prelim_pairs, data_PRE, data_POST, retakes_pre, retakes_post, prelim_instructor_change)
  print("Refined Match")

  comments_fill("PRE", no_matches_pre, data_PRE, data_PRE_dropped, retakes_pre, instructor_change)
  comments_fill("PST", no_matches_post, data_POST, data_POST_dropped, retakes_post, instructor_change)
  print("Filled comments")

  data_PRE, data_POST = standardize(data_PRE, "PRE"), standardize(data_POST, "PST")
  print("Standardized PRE and PST data")

  print("Merging...")
  merged_data = merger(no_matches_pre, no_matches_post, data_PRE, data_POST, data_PRE_dropped, data_POST_dropped, pairs, retakes_pre, retakes_post)
  merged_data_pub = public_merged(merged_data, data_PRE)
  public_data = public_data_anonym(merged_data_pub, retakes_pre, retakes_post, len(pairs), len(no_matches_pre), len(no_matches_post), test_administered_date)
  private_data = anonym_adder(len(data_PRE.columns), merged_data, public_data)
  private_data.to_csv(PREdata[:-4] +'_merged.csv', encoding='utf-8', index = False)
  public_data.to_csv(PSTdata[:-4]+'_merged.csv', encoding='utf-8', index = False)

if __name__ == '__main__':
  # legacy_run()
  run()
