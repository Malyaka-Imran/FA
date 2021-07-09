from repeats import repeats
import pandas as pd
import numpy as np
import pickle
import copy

def merge(nomatch_pre, nomatch_post, df_pre, df_post, pairs):
    '''
    Returns a single Pandas DataFrame from Pre and Post DataFrames

    Required functions:
        repeats
        col_index

    Args:
        nomatch_pre: Python list of int row indices of inputs in the pre-semester dataset.
        nomatch_post: Python list of int row indices of inputs in the post-semester dataset.
        df_pre: The Pandas DataFrame of the pre-semester dataset.
        df_post: The Pandas DataFrame of the post-semester dataset.
        pairs: Python int key dictionary of int row indices of matching pairs

    Returns:
        df_1: Pandas DataFrame

    Required modules:
        pandas as pd
        numpy as np

    By:
        Ilija Nikolov, 31.07.17
    Edited:
        Chloe Wohlgemuth, 01.08.20

    '''
    df = pd.DataFrame()
    num_pre_col = len(df_pre.columns)
    num_post_col = len(df_post.columns)
    # Indices of the pre and post dataframe columns
    columns_pre = df_pre.columns.tolist()
    columns_post = df_post.columns.tolist()

    # Get the list of column names, for PRE and PST DF
    columns = columns_pre + columns_post
    print("starting pairs")
    # Add by row for the pairs section of the dataframes
    for i in range(len(pairs)):
        df_pre.loc[pairs[i][0], "PRE_WHICHADMIN"] = 2
        df_post.loc[pairs[i][1], "PST_WHICHADMIN"] = 2
        left = df_pre.loc[pairs[i][0],:]
        right = df_post.loc[pairs[i][1],:]
        concat = pd.concat([left,right], ignore_index=True,axis=0)
        df = df.append(concat, ignore_index=True)
    print("first for loop done")
    # Add by row for the pre-nomatches
    for i in range(len(nomatch_pre)):
        df_pre.loc[nomatch_pre[i], "PRE_WHICHADMIN"] = 0
        left = df_pre.loc[nomatch_pre[i],:]
        right = pd.Series(np.nan, columns_post)
        concat = pd.concat([left,right], ignore_index=True,axis=0)
        df = df.append(concat, ignore_index=True)
    numCol_df = len(df.columns)
    print("second for loop")
    # Add by row for the post-nomatches
    for i in range(len(nomatch_post)):
        df_post.loc[nomatch_post[i], "PST_WHICHADMIN"] = 1
        left = pd.Series(np.nan, columns_pre)
        right = df_post.loc[nomatch_post[i],:]
        concat = pd.concat([left,right], ignore_index=True,axis=0)
        df = df.append(concat, ignore_index=True)
    df = df.iloc[:,0:numCol_df]
    print("creating big df")
    # Create one big dataframe with the right column names
    df_1 = pd.DataFrame(data = pd.DataFrame.to_numpy(df), columns=columns)
    print("allocate empty rows")
    # Allocate (empty for now) columns for info that will be imported from the instructor db
    df_1[['MRG_CRS_TYP','MRG_CRS_SUBJ','MRG_SCHL_TYPE','MRG_CRS_CRED']] = np.nan

    # Make merged effort flag + Collapse each of student ID and Response ID into one column
    df_1['MRG_EFFBOTH'] = np.nan
    df_1['STUDENT_ID'] = df_1['PRE_STUDENT_ID']
    df_1['RESPONSE_ID'] = df_1['PRE_ResponseId']
    for i in range(len(df_1)):
        if(df_1.loc[i, 'PRE_EFFFLAG'] == 1 and df_1.loc[i, 'PST_EFFFLAG'] == 1):
            df_1.loc[i,'MRG_EFFBOTH'] = 1
        if(pd.isnull(df_1.loc[i, 'STUDENT_ID'])):
            df_1.loc[i,'STUDENT_ID'] = df_1.loc[i,'PST_STUDENT_ID']
        if(pd.isnull(df_1.loc[i, 'RESPONSE_ID'])):
            df_1.loc[i,'RESPONSE_ID'] = df_1.loc[i,'PST_ResponseId']
    
    # Order the column names
    print("smth about pickle")
    with open('nameorder.pkl', 'rb') as f:
        nameorder = pickle.load(f)

    df_pub_cut = df_1[nameorder]
    df_pub = copy.deepcopy(df_pub_cut)
    print("this is the end")
    return df_pub