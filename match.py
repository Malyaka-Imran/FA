
def match(PREdata, PSTdata):
    '''
    A matching algorithm that matches on _STUDENT_ID column

    Args:
        PREdata: The Pandas DataFrame of the pre-semester dataset.
        PSTdata: The Pandas DataFrame of the post-semester dataset.

    Returns:
        PRE_not_matched: a Python list of int row-indeces for names that did not match in the pre data

        PST_not_matched: a Python list of int row-indeces for names that did not match in the post data

        pairs: a Python dictionary with int keys of int row-indeces for names that matched. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.

        instructor_change: a Python dictionary with int keys of int row-indeces for students that changed instructors. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.
    
    By:
        Chloe Wohlgemuth 01.05.21

    (previous O(n^2) version was by Ilija Nikolov, 17.07.17 and edited by Your friendly neighborhood Camilo Ortiz (August 5th, 2019))
    '''
    # Intermediary Variables
    PRE_IDs = list(PREdata['PRE_STUDENT_ID'].dropna().values) # list of PRE_STUDENT_IDs
    PST_IDs = list(PSTdata['PST_STUDENT_ID'].dropna().values) # list of PST_STUDENT_IDs
    PRE_not_matched_IDs = list(set(PRE_IDs) - set(PST_IDs)) # indices with a Student_ID in PST but not in PRE
    PST_not_matched_IDs = list(set(PST_IDs) - set(PRE_IDs)) # indices with a Student_ID in PRE but not in PST
    matched_IDs = list(set(PRE_IDs) - set(PRE_not_matched_IDs)) # Those with a Student_ID in both

    # Entries (indices) for returned non-match lists
    PRE_not_matched = list(map(lambda ID: PREdata.index[PREdata['PRE_STUDENT_ID'] == ID], PRE_not_matched_IDs))
    PST_not_matched = list(map(lambda ID: PSTdata.index[PSTdata['PST_STUDENT_ID'] == ID], PST_not_matched_IDs))
    
    # Returned pairs and instructor_change variables
    instructor_change = {}
    pairs = {}
    
    for ID in matched_IDs:
        # Update data variables
        PRE_index = PREdata.index[PREdata['PRE_STUDENT_ID'] == ID].values[0]
        PST_index = PSTdata.index[PSTdata['PST_STUDENT_ID'] == ID].values[0]
        pairs.update({len(pairs): (PRE_index, PST_index)})
        # Record changes in instructor
        if(PREdata.loc[PRE_index,"PRE_INSTR_ID"] != PSTdata.loc[PST_index,"PST_INSTR_ID"]):
            instructor_change.update({len(instructor_change): (PRE_index, PST_index)})

    return (PRE_not_matched, PST_not_matched, pairs, instructor_change)