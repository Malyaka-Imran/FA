from factor_analyzer import FactorAnalyzer, Rotator, calculate_bartlett_sphericity, calculate_kmo
from sklearn.utils import check_array
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def factor_analysis(database, semester, year, season, savedname):
    question = semester + "_Q" # question = 'PRE_Q' or 'PST_Q'

    data = pd.read_csv(database, encoding = 'utf-8', skiprows = [1,2], header = 0)
    df = pd.read_csv(answer_key, encoding = 'utf-8')


    cols = list(data.columns.values)
    c = len(cols)
    e = 0
    h = len(data)

    for d in range(c):
        column = cols[d]
        column = column[0:5]

        if question == column:
            e = e + 1
# Factor Analysis!
if(semester == "PRE" and e == 50) or (semester == "PRE" and e == 54):
    print("")
    '''
    # Variable selection
    att_data = data.loc[ data[semester + '_COMPFLAG']==1 ]
    att_data = att_data[att]

    # Drop all rows with NaN values
    att_data.dropna(inplace=True)

    loadings = rotator.fit_transform(fa.loadings_)

    # Set FA loadings to be rotator loadings
    fa.loadings_ = loadings
    #print (loadings)

    # Get factor scores
    factor_scores = fa.transform(att_data)
    factor_scores = pd.DataFrame(data=factor_scores, index=att_data.index, columns=["Factor "+str(i+1) for i in range(n_factors)])

    for i in factor_scores.index:
        data.at[i, semester + '_SELFEFF'] = factor_scores.at[i, 'Factor 1']
        data.at[i, semester + '_SCHMATH'] = factor_scores.at[i, 'Factor 2']
        data.at[i, semester + '_ACADMAT'] = factor_scores.at[i, 'Factor 3']
        data.at[i, semester + '_MATHREL'] = factor_scores.at[i, 'Factor 4']
        data.at[i, semester + '_MATHANX'] = factor_scores.at[i, 'Factor 5']'''

elif(semester == "PRE"):
    # Fill out whymajs with 0 instead of NaN values so we can
    # perform FA on them
    nan_columns = [semester + "_WHYMAJ_1", semester + "_WHYMAJ_2", semester + "_WHYMAJ_3",
        semester + "_WHYMAJ_4", semester + "_WHYMAJ_5", semester + "_WHYMAJ_6",
        semester + "_WHYMAJ_7", semester + "_WHYMAJ_8", semester + "_WHYCS_1",
        semester + "_WHYCS_2", semester + "_WHYCS_3", semester + "_WHYCS_4",
        semester + "_WHYCS_5", semester + "_WHYCS_6", semester + "_WHYCS_7"
    ]
    for i in data.index:
        for column in nan_columns:
            if pd.isna(data.at[i, column]):
                data.at[i, column] = 0

    # Factor Analysis variables
    att = [semester + '_FREQEN', semester + '_DAILYM', semester + '_DAILYG',
        semester + '_ATT_DL_3', semester + '_ATT_SC_1', semester + '_ATT_SC_2',
        semester + '_ATT_SC_4', semester + '_ATT_SC_5', semester + '_LK1',
        semester + '_LK2', semester + '_LK5', semester + '_ANX#1_1',
        semester + '_ANX#1_2', semester + '_ANX#1_3', semester + '_ANX#1_4',
        semester + '_CF_TOTAL', semester + '_ATT_DL_2', semester + '_ATT_SC_3',
        semester + "_WHYCS_1", semester + "_WHYCS_3", semester + "_WHYCS_5",
        semester + "_WHYCS_6", semester + "_EFFORT"
    ]

    # Variable selection
    att_data = data.loc[ data[semester + '_COMPFLAG']==1 ]
    att_data = att_data[att]
    # Drop all rows with NaN values
    att_data.dropna(inplace=True)

    swapList = ['_ATT_DL_2', '_ATT_DL_3', '_ATT_SC_1', '_ATT_SC_2',
        '_ATT_SC_3', '_ATT_SC_4', '_ATT_SC_5'
    ]
    for i in att_data.index:
        for col in swapList:
            swapOrdering(att_data, i, semester + col)

    # KMO and Barlett tests
    X = att_data.copy().values
    X = check_array(X, force_all_finite='allow-nan')

    statistic, p_value = calculate_bartlett_sphericity(X)
    #print("\nBarlett sphericity p={0}".format(p_value))
    kmo_per_variable, kmo_total = calculate_kmo(X)
    #print("Kaiser-Meyer-Olkin measure of sampling adequacy = {0}\n".format(kmo_total))

    # Create factor analysis object and perform factor analysis
    # Using maximum likelihood analysis (ml)
    n_factors = 5
    fa = FactorAnalyzer(rotation=None, n_factors=n_factors, method="ml")
    fa.fit(att_data)

    # Kaiser normalization and oblimin rotation
    rotator = Rotator(method="oblimin", normalize=True, max_iter=25)
    loadings = rotator.fit_transform(fa.loadings_)

    # Set FA loadings to be rotator loadings
    fa.loadings_ = loadings
    #print (loadings)

    # Get factor scores
    factor_scores = fa.transform(att_data)
    factor_scores = pd.DataFrame(data=factor_scores, index=att_data.index, columns=["Factor "+str(i+1) for i in range(n_factors)])
    #print("\nFactor scores: \n", factor_scores)

    factor_names = ["Numerical Self Efficacy", "School Math",
        "Academic maturity", "Numerical Relevancy", "Math Anxiety"]
    # Convert factor loadings to a df
    loadings = pd.DataFrame(data=loadings, index=att, columns=factor_names)

    # Drop non-meaningful values
    loadings = loadings.where(abs(loadings) > 0.32)
    #print("Factor loadings: \n", loadings)

    scores1 = factor_scores['Factor 1'].tolist()
    plt.hist(scores1, bins=[x for x in np.arange(-4.0, 4.0, 0.2)])
    plt.title("Numerical Self Efficacy")
    #plt.show()

    scores2 = factor_scores['Factor 2'].tolist()
    plt.hist(scores2, bins=[x for x in np.arange(-4.0, 4.0, 0.2)])
    plt.title("School Math")
    # plt.show()

    scores3 = factor_scores['Factor 3'].tolist()
    plt.hist(scores3, bins=[x for x in np.arange(-4.0, 4.0, 0.2)])
    plt.title("Academic maturity")
    # plt.show()

    scores4 = factor_scores['Factor 4'].tolist()
    plt.hist(scores4, bins=[x for x in np.arange(-4.0, 4.0, 0.2)])
    plt.title("Numerical Relevancy")
    # plt.show()

    scores5 = factor_scores['Factor 5'].tolist()
    plt.hist(scores5, bins=[x for x in np.arange(-4.0, 4.0, 0.2)])
    plt.title("Math Anxiety")
    # plt.show()
    # Update composite variables
    for i in factor_scores.index:
        data.at[i, semester + '_SELFEFF'] = factor_scores.at[i, 'Factor 1']
        data.at[i, semester + '_SCHMATH'] = factor_scores.at[i, 'Factor 2']
        data.at[i, semester + '_ACADMAT'] = factor_scores.at[i, 'Factor 3']
        data.at[i, semester + '_MATHREL'] = factor_scores.at[i, 'Factor 4']
        data.at[i, semester + '_MATHANX'] = factor_scores.at[i, 'Factor 5']
