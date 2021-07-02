from sklearn.utils import check_array
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def score(data, semester, year, season, answer_key):
    '''
    Edited for efficiency + documentation + robustness:
        Chloe Wohlgemuth, 01.08.21 + 02.04.21
    Modified so that it uses numerical values of question/answer rather than string values.
    By:
        Ilija Nikolov, 5 March 2018
    '''

    '''
        The score function reads in a QuaRCS dataset and answer key file to create a series of columns
        to add to the dataset. The function creates columns for:
        - score on a binary scale (1 for correct, 0 for incorrect)
        - total score
        - totals and means by category
        - number of questions answered
        - total and mean confidence
        Args:
            db: pre or post QuaRCS dataset for a semester
            answer_key: QuaRCS Assessment Answer Key
            semester: 'PRE' or 'PST'
        Output:
            name of file + '_scored' as .csv file
        Example:
            score('QuaRCS_Summer_2017_Pre.csv', 'PRE', QuaRCS Assessment Answer Key.csv', QuaRCS_Summer_2017_Pre )
            New File saved under QuaRCS_Summer_2017_Pre_scored.csv
            Check folder for files
        By:
            Abdoulaye Sanogo, 08/11/2017
        Future Improvements:
            add columns for confidence means and totals by category
            add extra colums after insert so the deletion of columns will not be necessary
    '''
    # Read in dataset
    preOrPost = semester + "_Q" # question = 'PRE_Q' or 'PST_Q'
    try:
        #data = pd.read_csv(db, encoding = 'utf-8', skiprows = [1,2], header = 0)
        df = pd.read_csv(answer_key, encoding = 'utf-8')
    except(UnicodeDecodeError):
        #data = pd.read_csv(db, encoding = 'ISO-8859-1', skiprows = [1,2], header = 0)
        df = pd.read_csv(answer_key, encoding = 'ISO-8859-1')
    
    columns = list(data.columns.values)
    numVariables = len(columns)
    numQuestions = 0
    numParticipants = len(data)
    #populate answer key
    corr_ans = {3:2, 5:2, 6:3, 7:4, 10:2, 11:1, 12:3, 13:2, 14:4, 15:3, 16:2, 19:2, 20:4,\
        21:1, 23:4, 26:2, 27:3, 28:2, 29:3, 30:1, 31:3, 32:4, 33:3, 34:4, 35:3}

    # Adds the Q#_SCORE column right next to each question
    for item in corr_ans.keys():
        if preOrPost+str(item) in data.columns:
            data.insert(data.columns.get_loc(preOrPost+str(item))+1,preOrPost+str(item)+'_SCORE', 0)

    # loops through all columns, figures out which columns correspond to test questions
    # fullOrLite >= 50 --> Full, fullOrLite < 50 --> Lite
    for var in range(numVariables):
        if preOrPost == columns[var][0:5]:
            numQuestions += 1
    
    # Questions Versioning
    data.insert(6, 'VERSION', " ")
    if numQuestions == 50:
        if(year == "16" and season == "Fa"):
            data['VERSION'] = "Fl_2.0"
            # If the value "progress bar" is in comments, change the version to 2.1
            for participant in range(numParticipants):
                if 'COMMENTS' in data.columns and (data.loc[participant, 'COMMENTS'] == "progress bar"):
                    data.loc[participant, 'VERSION'] = "Fl_2.1"
        else:
            data['VERSION'] = "Fl_1.1"
    elif numQuestions == 54:
        data['VERSION'] = "Fl_1.0"
        to_drop = [semester+'_Q18',semester+'_Q18CF',semester+'_Q25',semester+'_Q25CF']
        data = data.drop(to_drop, axis=1)
        numQuestions = 50
    elif numQuestions == 22:
        data['VERSION'] = "Lt_1.0"
    elif numQuestions == 30 or numQuestions == 45:
        if (int(year) >= 19 or (year == "18" and season == "Fa")):
            data['VERSION'] = "Lt_2.1"
        else:
            data['VERSION'] = "Lt_2.0"
    elif numQuestions == 28:
        data['VERSION'] = "SM_1.0"

    # Allocating space (new columns) for variables
    totals = ['_TOTAL','_PCT_TOTAL','_GR_TOTAL','_GR_MEAN','_AR_TOTAL','_AR_MEAN','_PR_TOTAL',\
        '_PR_MEAN','_PC_TOTAL','_PC_MEAN','_SP_TOTAL','_SP_MEAN','_TR_TOTAL','_TR_MEAN',\
            '_AV_TOTAL','_AV_MEAN','_UD_TOTAL','_UD_MEAN','_ES_TOTAL','_ES_MEAN'] # Totals
    compos = ['_SELFEFF','_MATHANX','_MATHREL','_ACADMAT','_SCHMATH'] # Composite Variables
    conf = ['_CF_TOTAL','_CF_TOTAL_CORR','_CF_TOTAL_INCORR','_CF_MEAN','_CF_MEAN_CORR','_CF_MEAN_INCORR'] # Confidence Metrics
    com_eff = ['_QCOMPLETE','_COMPFLAG','_EFFFLAG'] # Completion and Effort Variables
    cols = [semester + s for s in compos+conf+com_eff]
    data[cols] = np.nan
    
    def scoringTotalsAndMeans(participant, semester, gradedAns, numCorrect):
        ''' Adds totals and means to their respective columns '''
        GR = pd.Series([gradedAns[i] for i in [15,14,12,29,30,13]]).dropna()
        GRsum = GR.sum()
        AR = pd.Series([gradedAns[i] for i in [15,14,26,27,23,28,19,3,16,31,32,5,6,7,29,30,10,11,20,21,33,34,35]]).dropna()
        ARsum = AR.sum()
        PR = pd.Series([gradedAns[i] for i in [15,12,14,23,28,3,16,7,10,11,20,21,33,35,13]]).dropna()
        PRsum = PR.sum()
        PC = pd.Series([gradedAns[i] for i in [27,3,32,20,21]]).dropna()
        PCsum = PC.sum()
        SP = pd.Series([gradedAns[i] for i in [27,23,28,29,30,20,21]]).dropna()
        SPsum = SP.sum()
        TR = pd.Series([gradedAns[i] for i in [26,27,23]]).dropna()
        TRsum = TR.sum()
        AV = pd.Series([gradedAns[i] for i in [31,10,11,33,34]]).dropna()
        AVsum = AV.sum()
        UD = pd.Series([gradedAns[i] for i in [31,6,7,35,16]]).dropna()
        UDsum = UD.sum()
        ES = pd.Series([gradedAns[i] for i in [15,12,14,16,13]]).dropna()
        ESsum = ES.sum()

        # sum of correct scores
        data.loc[participant, semester + '_GR_TOTAL'] = GRsum
        data.loc[participant, semester + '_AR_TOTAL'] = ARsum
        data.loc[participant, semester + '_PR_TOTAL'] = PRsum
        data.loc[participant, semester + '_PC_TOTAL'] = PCsum
        data.loc[participant, semester + '_SP_TOTAL'] = SPsum
        data.loc[participant, semester + '_TR_TOTAL'] = TRsum
        data.loc[participant, semester + '_AV_TOTAL'] = AVsum
        data.loc[participant, semester + '_UD_TOTAL'] = UDsum
        data.loc[participant, semester + '_ES_TOTAL'] = ESsum

        # mean score
        data.loc[participant, semester + '_TOTAL'] = numCorrect
        data.loc[participant, semester + '_PCT_TOTAL'] = numCorrect / (numQuestions / 2)
        data.loc[participant, semester + '_GR_MEAN'] = GRsum / GR.size
        data.loc[participant, semester + '_AR_MEAN'] = ARsum / AR.size
        data.loc[participant, semester + '_PR_MEAN'] = PRsum / PR.size
        data.loc[participant, semester + '_PC_MEAN'] = PCsum / PC.size
        data.loc[participant, semester + '_SP_MEAN'] = SPsum / SP.size
        data.loc[participant, semester + '_TR_MEAN'] = TRsum / TR.size
        data.loc[participant, semester + '_AV_MEAN'] = AVsum / AV.size
        data.loc[participant, semester + '_UD_MEAN'] = UDsum / UD.size
        data.loc[participant, semester + '_ES_MEAN'] = ESsum / ES.size

    def confidenceMetrics(participant, semester, confidenceInEachAnswer,gradedAns, numQuestions):
        totalConfidence = 0
        corrscore = 0
        incorrscore = 0
        confcount = 0
        for item in confidenceInEachAnswer:
            totalConfidence += confidenceInEachAnswer[item]

            if confidenceInEachAnswer[item] > 0:
                confcount +=1
                if(gradedAns[item] == 1):
                    corrscore += confidenceInEachAnswer[item]
                else:
                    incorrscore += confidenceInEachAnswer[item]
        #print(confcount)
        if (confcount == 0):
            confcount = 1
        # Student's score
        numcorr = data.loc[participant, semester + '_TOTAL']

        # Calculate confidence scores
        data.loc[participant, semester + '_CF_TOTAL'] = totalConfidence
        data.loc[participant, semester + '_CF_TOTAL_CORR'] = np.nan if (numQuestions == 22 or numQuestions == 28) else corrscore
        data.loc[participant, semester + '_CF_TOTAL_INCORR'] = incorrscore
        data.loc[participant, semester + '_CF_MEAN'] = totalConfidence/confcount

        if numcorr != 0:
            data.loc[participant, semester + '_CF_MEAN_CORR'] = corrscore/numcorr
        else:
            data.loc[participant, semester + '_CF_MEAN_CORR'] = 0
        if numcorr != confcount:
            data.loc[participant, semester + '_CF_MEAN_INCORR'] = incorrscore/(confcount-numcorr)
        else:
            data.loc[participant, semester + '_CF_MEAN_INCORR'] = 0


    def checkCompletion(participant,questionList):
        total = 0
        for question in questionList:
            count = preOrPost + str(question)

            answered = data.loc[participant, count]
            if (str(answered) == 'nan' or str(answered) == ' '):
                continue
            else:
                total += 1

        data.loc[participant, semester + '_QCOMPLETE'] = total

        # Add completed flag
        if total == len(questionList):
            data.loc[participant, semester + '_COMPFLAG'] = 1
        else:
            data.loc[participant, semester + '_COMPFLAG'] = 0

    eff_scores = {1:0, 2:0, 3:0.5, 4:1, 5:1, "I didn’t try very hard":0, "I tried for a while and then got bored":0, "I tried pretty hard":0.5, "I tried my best on all or most of the questions":1}
    def scoreEffort(participant, semester):        
        #import pdb;pdb.set_trace()
        effort_response = data.loc[participant, semester + '_EFFORT']
        if (pd.isnull(effort_response)): # If there is no response for effort, mark completion as 0 for that student!
            data.loc[participant, semester + '_COMPFLAG'] = 0
        else: #full marks for high effort, partial for some effort, 0 for no effort
            data.loc[participant, semester + '_EFFFLAG'] = eff_scores[effort_response]
    
    for participant in range(numParticipants):
        questionList = [] # list of question numbers, depending on the version of the test
        gradedAns = {3:0, 5:0, 6:0, 7:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15: 0, 16:0, 19:0, 20:0, 21:0, 23:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0, 32:0, 33:0, 34:0, 35:0}
        confidenceInEachAnswer = gradedAns.copy()
        numCorrect = 0
        for q_num in gradedAns: #grade answers for each participant
            try:
                if str(preOrPost + str(q_num)) in data.columns: # question is in survey version
                    questionList.append(q_num)
                    confidenceInEachAnswer[q_num] = int(data.loc[participant, preOrPost + str(q_num) + "CF"])
                    if(int(data.loc[participant, preOrPost + str(q_num)]) == corr_ans[q_num]):
                        gradedAns[q_num] = 1
                        data.loc[participant, preOrPost+str(q_num)+'_SCORE'] = 1
                        numCorrect += 1
            except: # i.e. NaN due to unanswered question or participant entries to be dropped
                pass

        #populates dataframe with correct answer totals and 
        scoringTotalsAndMeans(participant,semester,gradedAns,numCorrect)
        #populates dataframe with confidence metrics
        confidenceMetrics(participant, semester, confidenceInEachAnswer,gradedAns,numQuestions)
        #checks if a participant has answered all the questions
        checkCompletion(participant,questionList)
        #scores effort
        scoreEffort(participant, semester)
        #lacks number of questions for meaningful score
        if numQuestions == 22: # 1 q, 2 qs, 1 q
            cols = [semester+'_UD_MEAN', semester+'_UD_TOTAL',semester+'_PC_MEAN',semester+'_PC_TOTAL',semester+'_AV_MEAN',semester+'_AV_TOTAL']
            data.loc[participant,cols] = np.nan
        elif numQuestions == 30: # 1 q, 2 qs
            cols = [semester+'_UD_MEAN', semester+'_UD_TOTAL',semester+'_PC_MEAN',semester+'_PC_TOTAL']
            data.loc[participant,cols] = np.nan
        elif numQuestions == 28: # 2 q, 1 q
            cols = [semester+'_TR_MEAN',semester+'_TR_TOTAL',semester+'_AV_MEAN',semester+'_AV_TOTAL']
            data.loc[participant,cols] = np.nan

    return data