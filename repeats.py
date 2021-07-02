import pandas as pd
import numpy as np


def repeats(df, semester):
    '''
    Identifies all repeat administrations of the exam to an individual student.
    Their first complete assessment is retained and passed on, while a file containing
    all exams taken by students who took repeat administrations is also produced.

    Returns DataFrame without repeat administrations and a .csv of all repeat administrations.
        * Names must be approximately similar (i.e. no spelling mistakes, no extra names).

    Required functions:
        col_index

    Args:
        df: The Pandas DataFrame in question.
        semester: PRE/PST

    Returns:
        df
        Repeats.csv
            * Example: PRE_S18_Repeats.csv

    Future improvements:
        Better name-matching mechanism.

    By:
        Chloe Wohlgemuth 01.06.21

    (original O(n^2) + less efficient version by Ilija Nikolov, 20.07.17)
    '''
    # df = pd.read_csv(df, encoding = 'utf-8', header = 0)
    # savedname = df[:-4]
    df = df.reset_index(drop=True)

    # slicing out the DataFrame for speed
    idList = df[semester + '_STUDENT_ID']

    # Create template DataFrame for repeats
    toExport = pd.DataFrame(df)
    toExport = toExport.iloc[0:0]

    ''' Algorithm '''
    def getDuplicates(lis):
        ''' Returns dict of locations for duplicate elements in list'''
        counts = dict()
        for ind in range(len(lis)):
            el = lis[ind]
            if el in counts:
                counts[el].append(ind) # Append newly-found location of element
            else:
                counts[el] = [ind] # Append first-time found element
        return counts
        
    # loop through all student IDs for duplicates
    repeats = getDuplicates(idList) # each entry: {ID, [index1, index2, etc.]}

    # Packaging and exporting the list of repeated ID's
    for x in list(repeats):
        length = len(repeats[x])
        if length < 2: # remove non-duplicates (elements occuring only once)
            del repeats[x]
        else:
            df.loc[x, semester+'_NUM_REPEATS'] = length # filling in df column '_NUM_REPEATS'
            toExport = toExport.append(df.loc[x], ignore_index = True)
            df = df.drop(index=repeats[x]) # drop duplicate indices (i.e. rows) from df

    # Uncomment to write repeats for export
    # toExport.to_csv(semester+"_repeats.csv", encoding='utf-8',index=False)
    # print("Saved repeat entries to " + semester+"_repeats.csv")

    # returns df without repeat administrations
    # df.to_csv(semester+"_test.csv", encoding='utf-8',index=False)

    return df


def col_index(df, col_name):
    '''
    Returns the index for the specified column from a given DataFrame. If the column appears more than once,
    it returns the index of lower indexed column.

    Args:
        df: The Pandas DataFrame containing the column.
        col_name: The str name of the column, must be exact as it appears in the df.

    Returns:
        An int column index.

    Examples:
        >>> col_index(df_pre, 'Firstname')
        31

    Future improvements:
        Column name error tolerance.

    By:
        Ilija Nikolov, 30.07.17

    '''
    #If the column appears only once, pandas.get_loc returns the desired int
    if (type(df.columns.get_loc(col_name)) == int):
        i = df.columns.get_loc(col_name)

    #Otherwise, pd.get_loc returns a boolean mask
    else:
        for i in range(len(df.columns)):
            #First time a column is seen, the for cycle stops
            if (df.columns.get_loc(col_name)[i] == True):
                break

    #returns the column index
    return i
