def id_gen(data_name, semester, year, season, stu_db_name, instr_db_name):
    import pandas as pd
    student_ID_DB = pd.read_csv(stu_db_name, encoding = 'utf-8')
    instr_ID_DB = pd.read_csv(instr_db_name, encoding = 'utf-8')

    # data = pd.read_csv(data_name, encoding = 'utf-8')
    # new_data_name = data_name.name + "_id.csv"
    data = data_name

    ind = col_index(data, (semester + "_SCHOOL"))

    data.insert((ind + 1) ,semester + '_INSTR_ID', " ")
    data.insert((ind + 4) ,semester + '_STUDENT_ID', " ")

    data = data.sample(frac=1).reset_index(drop=True)

    data_1, stu_ID_prelim, check, track = stu_id_match(data, semester, year, student_ID_DB)
    data_2, stu_ID_new = stu_id_match_refine(data_1, semester, year, stu_ID_prelim, check, track)

    data_3, instr_ID_new, check, track = instr_id_match(data_2, semester, year, season, instr_ID_DB)

    data_3 = data_3.drop([semester + '_INSTR'], axis=1)
    data_3 = data_3.drop([semester + '_Firstname'], axis=1)
    data_3 = data_3.drop([semester + '_Lastname'], axis=1)

    #data_3.to_csv(semester + "_thing.csv", encoding='utf-8',index=False)
    stu_ID_new.to_csv(stu_db_name, encoding='utf-8',index=False)
    instr_ID_new.to_csv(instr_db_name, encoding='utf-8',index=False)

    return data_3

def str_simplify(some_string):
    '''
    Simplifies a string (str) to an alphabet-only and lowercase-only (a-z) str.

    Args:
        some_string: The string in question.

    Returns:
        A super-simplified str.

    Examples:
        >>> str_simplify('A1m0H()** % 55Er+"s"+t'' @')
        'amherst'

    Future improvements:
        Fix possible problems with multiple apostrophes mid string.

    By:
        Ilija Nikolov, 20.07.17
    '''
    some_string = str(some_string)
    some_string = some_string.lower()

    #removes any special characters, whitespaces and capitalizations
    some_string = ''.join(e for e in some_string if e.isalnum())

    #removes any digit in a string
    some_string = ''.join(i for i in some_string if not i.isdigit())

    return some_string

def stu_id_match(data_old, semester, year, dB_old):
    import copy
    import pandas as pd
    import numpy as np
    data = copy.deepcopy(data_old)
    dB = copy.deepcopy(dB_old)

#initialize variables for storing
    track = 1
    if(len(dB) != 0):
        findtrack = (dB.loc[(len(dB)-1),"STUDENT_ID"])
        if(findtrack[:3] == ("S" + year)):
            track = int(findtrack[3:]) + 1
    noEmail = False
    check = []
    #incheck = []

#slicing out the dataframes for speed

    fst_id = semester + '_Firstname'
    lst_id = semester + '_Lastname'
    eml_id = semester + '_EMAIL'
    schl_id = semester + '_SCHOOL'
    stu_id = semester + '_STUDENT_ID'

    if(data[eml_id].isnull().all()):
        noEmail = True
    the_list = [fst_id, lst_id, schl_id, eml_id, stu_id]
    work_data = data[the_list]

    #begin matching
    for i in work_data.index:
        newS = True
        fst = str_simplify(work_data.loc[i, fst_id])
        lst = str_simplify(work_data.loc[i, lst_id])
        schl = work_data.loc[i,schl_id]
        eml = np.nan
        if (noEmail == False):
            #print("There are emails!")
            #print(work_data.loc[i, eml_id])
            if (work_data.loc[i, eml_id] != np.nan):
                eml = (work_data.loc[i, eml_id]).lower()
                for j in range (len(dB)):
                    if (dB.loc[j, "EMAIL"] == eml):
                        data.loc[i, stu_id] = dB.loc[j, "STUDENT_ID"]
                        newS = False
                        break
        if (newS):
            for j in range (len(dB)):
                if (dB.loc[j, "Lastname"] == lst and dB.loc[j, "Firstname"] == fst and dB.loc[j, "SCHOOL"] == schl):
                    if(noEmail == False):
                        if (pd.isnull((dB.loc[j, "EMAIL"]))):
                            dB.loc[j, "EMAIL"] = eml
                        elif((dB.loc[j, "EMAIL"]).split('.')[-1] != "edu" and eml.split('.')[-1] == "edu"):
                            dB.loc[j, "EMAIL"] = eml
                        elif(len((dB.loc[j, "EMAIL"]).split('.')) == 1):
                            dB.loc[j, "EMAIL"] = eml
                    data.loc[i, stu_id] = dB.loc[j, "STUDENT_ID"]
                    newS = False
                    break

        if (newS):
            for j in range (len(dB)):
                if(dB.loc[j, "Lastname"] == lst and (dB.loc[j, "Firstname"])[:2] == fst[:2] and dB.loc[j, "SCHOOL"] == schl):
                    #fn = str(dB.loc[j, "Firstname"] + ", " + fst)
                    #if(fn not in incheck)
                    check.append((i,j))
                        #incheck.append(fn)
                    data.loc[i, stu_id] = " "
                    newS = False
        if (newS):
            newstu = [fst, lst, eml, schl, newID(track, year)]
            track += 1
            data.loc[i, stu_id] = newstu[4]
            dB.loc[len(dB)] = newstu
    return data, dB, check, track

def instr_id_match(data_old, semester, year, season, dB_old):
    import copy
    import pandas as pd
    import numpy as np
    data = copy.deepcopy(data_old)
    dB = copy.deepcopy(dB_old)

#initialize variables for storing
    track = 1
    if(len(dB) != 0):
        findtrack = (dB.loc[(len(dB)-1),"INSTR_ID"])
        if(findtrack[:3] == ("I" + year)):
            track = int(findtrack[3:]) + 1
    check = []

#slicing out the dataframes for speed

    nm_id = semester + '_INSTR'
    crs_id = semester + '_COURSE'
    schl_id = semester + '_SCHOOL'
    instr_id = semester + '_INSTR_ID'

    the_list = [nm_id, crs_id, schl_id, instr_id]
    work_data = data[the_list]

    admin = season + year
#begin matching

    instr_list = []
    for i in work_data[nm_id]:
        if(isinstance(i, str) and (i not in instr_list)):
            instr_list.append(i)
    for i in instr_list:
        newI = True
        nm = i
        i_id = ""
        lst = ""
        fst = ""

        if (',' in nm):
            splt = nm.split(", ")
            fst = str_simplify(splt[1])
            lst = str_simplify(splt[0])
        else:
            splt = nm.split(" ")
            lst = str_simplify(splt[1])
            fst = str_simplify(splt[0])

        for j in range (len(dB)):
            if (dB.loc[j, "Lastname"] == lst and dB.loc[j, "Firstname"] == fst):
                i_id = dB.loc[j, "INSTR_ID"]
                newI = False
        if(newI):
            i_id = newID_instr(track, year)
            track += 1
            newinstr = [nm, fst, lst, i_id]
            dB.loc[len(dB)] = newinstr

        for j in work_data.index:
            if (work_data.loc[j, nm_id] == nm):
                data.loc[j, instr_id] = i_id
                continue

    return data, dB, check, track

def newID(trk, yr):
    num = trk
    num = str(num)
    while(len(num) < 5):
        num = "0" + num
    return ("S"+ yr + num)

def newID_instr(trk, yr):
    num = trk
    num = str(num)
    while(len(num) < 3):
        num = "0" + num
    return ("I"+ yr + num)

def stu_id_match_refine(data_old, semester, year, dB_old, check, track):
    import copy
    import pandas as pd
    import numpy as np
    data = copy.deepcopy(data_old)
    dB = copy.deepcopy(dB_old)
    noEmail = True
    if((semester + "_EMAIL") in data.columns):
        noEmail = False
    for i in check:

        fst1 = str_simplify(data.loc[i[0], semester + "_Firstname"])
        lst1 = str_simplify(data.loc[i[0], semester + "_Lastname"])
        eml1 = np.nan
        schl1 = data.loc[i[0], semester + "_SCHOOL"]
        fst2 = dB.loc[i[1], "Firstname"]

        #if(dB.loc[i[1], "Lastname"] == data.loc[i[0], "Lastname"] and (dB.loc[i[1], "Firstname"])[:2] == data.loc[(i[0]), "Firstname"][:2] and dB.loc[i[1], "SCHOOL"] == data.loc[i[0], "SCHOOL"]):

        if(ask_conf(fst2, fst1, lst1)):
            if(noEmail == False):
                eml1 = data.loc[i[0], semester + "_EMAIL"]
                eml2 = dB.loc[i[1], "EMAIL"]
                if (pd.isnull(eml2)):
                    dB.loc[i[1], "EMAIL"] = eml1
                elif(eml2.split('.')[-1] != "edu" and eml1.split('.')[-1] == "edu"):
                    dB.loc[i[1], "EMAIL"] = eml1
                elif(len(eml2.split('.')) == 1):
                    dB.loc[i[1], "EMAIL"] = eml1
            data.loc[i[0], (semester + "_STUDENT_ID")] = dB.loc[i[1], "STUDENT_ID"]

        else:
            newstu = [fst1, lst1, eml1, schl1, newID(track, year)]
            track += 1
            data.loc[i[0], (semester + "_STUDENT_ID")] = newstu[4]
            dB.loc[len(dB)] = newstu
    return data, dB


def ask_conf(nm1, nm2, ln):
    import sys
    "Code borrowed from: https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input"
    """Asks whether two strings look the same and returns the given answer.

    "nm1" is one firstname
    "nm2" is the other firstname
    "ln" is last name


    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [y/n] "

    while True:
        sys.stdout.write("Do you think these are the same person: " + nm1 + "/" + nm2 + " " + ln + "?" + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

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
        >>> col_index(data_pre, 'Firstname')
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
