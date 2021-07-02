import glob
import datetime 
import pandas as pd

print('Merging...')
# Collect names of all files in data file with .csv extension into a list
files = glob.glob('./Master_data_S20_*.csv', recursive = True)
print(files)

# Removing './' that are included in the file name
for n in files:
    i = files.index(n)
    files[i] = files[i].replace('./','')

# Combining all files into one data frame
data = pd.DataFrame()
for n in files:
    i = files.index(n)
    df = pd.read_csv(files[i])
    data = data.append(df)

# Receiving today's date
currentDT = datetime.datetime.now()
date = currentDT.strftime("_%Y_%m_%d")

# Exporting data frame as a .csv with today's date appended. 
export = data.to_csv(r'./Master_data'+ date +'.csv', index = None, header=True)
print('Merging complete')