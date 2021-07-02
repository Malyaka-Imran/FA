import pandas as pd
import numpy as np
import copy
import pickle

def clean(db, semester):
    '''
    Returns a cleaned version of the semester database
    '''
    #If file is being exported after clean module is run uncomment the following:
        # db = pd.read_csv(database, encoding = 'utf-8', header = 0)
        # savedname = database[:-4]

    # Opens the pickled list of column names for the appropriate semester
    if semester == "PRE":
        with open ('prelist.pkl', 'rb') as fp:
            col_list = pickle.load(fp)
    else:
        with open ('pstlist.pkl', 'rb') as fp:
            col_list = pickle.load(fp)

    # Makes new columns to be used later
    db[["INST_CHANGE","WHICHADMIN"]], db["NUM_REPEATS"] = np.nan, 1

    # Makes a full copy of the original data to be used during cleaning
    db_old = copy.deepcopy(db)
    # Replaces all the whitespace (of any length) cells with an np.nan
    db_old = db_old.applymap(lambda x: np.nan if isinstance(x, str) and x.isspace() else x)
    #accounting for old data with full-name provided in "NAME" column
    if 'NAME' in db_old.columns:
        #Create first name and last name columns
        db_old['Firstname'], db_old['Lastname'] = " ", " "

        #split using the whitespaces provided in name
        for i in range(len(db_old.iloc[:,col_index(db_old,'NAME')])):
            namestring = str(db_old.iloc[i,col_index(db_old,'NAME')]).strip()
            splt_names = namestring.split(" ")
            #firstname cell gets the first element
            db_old.iloc[i,col_index(db_old,'Firstname')] = splt_names[0]

            #the rest go to lastname cell
            name = ' '.join(splt_names)
            for j in range(len(splt_names)):
                name = name + ' ' + splt_names[j]
            db_old.iloc[i, col_index(db_old,'Lastname')] = name

        # makes list of column titles
        cols = list(db_old.columns.values)
        findex = cols.index('NAME')
        lindex = findex + 1

        # rearranges placement of columns
        cols.insert(findex, "Firstname")
        cols.insert(lindex, "Lastname")

        #deletes duplicates of column names
        del cols[-2] #deletes second to last object in list which is "First Name"
        del cols[-1] #deletes last object which is "Last Name"
        del cols[cols.index('NAME')]

        #Applies new column order
        db_old = db_old[cols]

    #accounting for full-name provided in one cell
    for i in range(len(db_old.iloc[:,col_index(db_old,'Firstname')])):

        #check if Firstname cell is empty
        if(pd.isnull(db_old.iloc[i,col_index(db_old,'Firstname')])):

            #skip if no name provided at all
            if(pd.isnull(db_old.iloc[i,col_index(db_old,'Lastname')])):
                continue

            #full-name is in the lastname cell
            else:
                #split using the whitespaces provided in the one cell
                namestring = str(db_old.iloc[i,col_index(db_old,'Lastname')]).strip()
                splt_names = namestring.split(" ")

                #firstname cell gets the first element
                db_old.iloc[i,col_index(db_old,'Firstname')] = splt_names[0]

                #the rest go to lastname cell
                name = ' '.join(splt_names)

                for j in range(len(splt_names)):
                    name = name + ' ' + splt_names[j]
                db_old.iloc[i, col_index(db_old, 'Lastname')] = name

        #firstname cell contains data
        else:
            #skip if lastname cell also contains data
            if(pd.notnull(db_old.iloc[i,col_index(db_old,'Lastname')])):
                continue

            #full-name name is in the firstname cell
            else:
                #split using the whitespaces provided in the one cell
                namestring = str(db_old.iloc[i,col_index(db_old,'Firstname')]).strip()
                splt_names = namestring.split(" ")

                #firstname cell gets the first element
                db_old.iloc[i,col_index(db_old,'Firstname')] = splt_names[0]

                #the rest go to lastname cell
                name =''
                for j in range(len(splt_names)):
                    name = name + ' ' + splt_names[j]
                db_old.iloc[i, col_index(db_old, 'Lastname')] = name

    #resets index of old data
    db_old.reset_index()
    #filtering out unfinished sessions
    db_trans = db_old[db_old[semester + '_COMPFLAG'] == 1]

    #filtering out sessions with no name provided
    db_provis = db_trans[pd.notnull(db_old['Firstname']) & pd.notnull(db_old['Lastname'])]

    #filtering out sessions with one character names
    db_interim = db_provis[(db_provis['Firstname'].str.len() > 1) & (db_provis['Lastname'].str.len() > 1)]

    #makes a copy of the data
    db_new = copy.deepcopy(db_interim)

    #gets lists of the indices in each database to figure out what rows were dropped
    index_old = db[db.columns[0]].index.tolist()
    index_new = db_new[db_new.columns[0]].index.tolist()

    df_1 = pd.DataFrame()
    for i in index_old:
        if(i not in index_new):
            df_1 = df_1.append(db.loc[i,:], ignore_index=True)
    data_dropped = pd.DataFrame(data=df_1, columns = db.columns.tolist())

    db_new = db_new.reset_index(drop=True)

    #fixes usedu column. Currently 2 = No, 1 = Yes, so will change to 2 = 0 = No
    for i in range(len(db_new)):
        if (semester == "PRE"):
            if 'PRE_USEDU' in db_new.columns:
                if(db_new.loc[i, 'PRE_USEDU'] == 2):
                    db_new.loc[i, 'PRE_USEDU'] = 0
            else:
                pass

    # Drop columns that have unnecessary information
    db_new = db_new.drop(['Status','UserLanguage','IPAddress','EndDate','DistributionChannel','Finished','RecordedDate','RecipientLastName','RecipientFirstName','RecipientEmail','ExternalReference'], axis=1)
    #db_new = db_new.drop(['META_INFO_Browser','META_INFO_Resolution','META_INFO_Version'], axis=1)

    #dropping columns unique to some versions
    db_new = db_new.drop(['LocationLatitude','LocationLongitude','PRE_YEAR_5_TEXT - Topics','Firstname - Topics'], axis=1, errors = 'ignore')

    #Add comments column if it isn't already there
    if ('COMMENTS' not in db_new.columns):
        db_new['COMMENTS'] = ""

    #Add PRE/PST to columns that don't have them in the name
    list = db_new.columns
    for i in range(len(list)):
        check = list[i].split("_")
        if(check[0] != semester):
            db_new.rename(columns={db_new.columns[i]: (semester + "_" + db_new.columns[i])}, inplace=True)

    #find instructor columns
    cols = db_new.columns
    for i in range(len(cols)):
        check = cols[i].split("_")
        if 'INSTR' in check:
            break

    inst_col = i
    #inserting blank columns in the appropriate location
    db_new.insert(inst_col, semester+'_COURSE', np.nan)
    db_new.insert(inst_col, semester+'_INSTR', np.nan)

    #for-loop to go through the columns for the individual instructors and collapse them into one column
    j = inst_col + 2
    check = cols[j].split("_")
    for i in range(len(db_new.iloc[:,inst_col])):
        if(not ((check[1]) == "INSTR" or (check[1]) == "PCCINS" or (check[1]) == "SFSU" or (check[1]) == "PCCCRS")):
            break
        if(pd.notnull(db_new.iloc[i,j])):
            if(pd.notnull(db_new.iloc[i,inst_col])):
                db_new.iloc[i,(inst_col + 1)] = db_new.iloc[i,j]
            else:
                db_new.iloc[i,(inst_col)] = db_new.iloc[i,j]
    j += 1
    check = cols[j].split("_")

    for i in range((inst_col + 2), j):
        db_new = db_new.drop(cols[i], axis=1)

    #standardizing columns using the pickled list imported earlier
    for i in col_list:
        data_list = db_new.columns
        if (i not in data_list):
            db_new.insert(0, i, np.nan)

    #reseting indices again
    db_new = db_new.reindex(sorted(db_new.columns), axis=1)

    # Uncomment to save to file
        #db_new.to_csv(savedname+"_cleaned.csv", encoding='utf-8',index=False)
        #db_new.to_csv(semester + "_thing.csv", encoding='utf-8',index=False)
        # print("Results saved to " + savedname + "_cleaned.csv")
    return db_new

    #Legacy Cleaning
    '''
    Returns an automatically polished DataFrame, where any rows containing no names,
    or one-character names are dropped and returned in SEMESTER_no_name.csv.
    It also checks if the name is provided in one cell and makes sure that it is split
    into the two cells - Firstname and Lastname.
    It adds logistical columns at the end of the DataFrame.
    Drops incomplete data and returns those rows in SEMESTER_incomplete.csv.

    Args:
        database: The Pandas DataFrame in question.
        semester: PRE/PST

    Returns:
        db_new: Pandas DataFrame that is automatically cleaned
        SEMESTER_incomplete.csv: File containing the incomplete rows
        SEMESTER_no_name.csv:	File containing rows with no name

    Future improvements:

    Required modules:
        import pandas as pd
        import numpy as np
        import copy

    Originally By:
        Ilija Nikolov, 30.07.17

    '''

    '''
    Returns the index for the specified column from a given DataFrame. If the column appears more than once,
    it returns the index of lower indexed column.

    Args:
        df: The Pandas DataFrame containing the column.
        col_name: The str name of the column, must be exact as it appears in the df.

    Returns:
        An int column index.

    Examples:
        >>> col_index(data_pre, 'Firstname')
        31

    Future improvements:
        Column name error tolerance.

    By:
        Ilija Nikolov, 30.07.17
        
    '''
def col_index(df, col_name):
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