import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from statsmodels.api import OLS

data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_scouting_amended.csv")

# Define "High-Quality Pass"
    # Two additional possession plays by the passer’s team, or one of: a “Carried” zone entry, any shot, any Goal
    # A possession of 3 or more seconds after entering the offensive zone
    # A penalty taken by the opposing team
def cte_HQ_Pass(idx_pass, df): # "idx_pass" are the indices of all 'Play' in "df"
    # return a series that will be appended to "df"
    return_df = df
    return_df['HQ_Pass'] = 'No'

    for index in idx_pass:
        try:
            event_after = df.loc[index + 1, 'Event']
            event_second_after = df.loc[index + 2, 'Event']

            if (((return_df.loc[index, 'Team'] == return_df.loc[index + 1, 'Team']) & (return_df.loc[index, 'Team'] == return_df.loc[index + 2, 'Team'])) | \
                ((return_df.loc[index + 1, 'Event'] == 'Zone Entry') & (return_df.loc[index + 1, 'Detail_1'] == 'Carried')) | \
                ((return_df.loc[index + 1, 'Event'] == 'Shot') | (return_df.loc[index + 1, 'Event'] == 'Goal')) | \
                ((return_df.loc[index + 1, 'Event'] == 'Penalty') & (return_df.loc[index, 'Team'] != return_df.loc[index + 1, 'Team'])) | \
                ((return_df.loc[index + 2, 'Event'] == 'Penalty') & (return_df.loc[index, 'Team'] != return_df.loc[index + 2, 'Team']))) & \
                (return_df.loc[index, 'Event'] == 'Play'):
                    return_df.loc[index, 'HQ_Pass'] = 'Yes'
        except:
            print("")

    return return_df.loc[(return_df['Event'] == 'Play') | (return_df['Event'] == 'Incomplete Play'),]

index_of_passes = data.loc[(data['Event'] == 'Play') | (data['Event'] == 'Incomplete Play')].index
result = cte_HQ_Pass(index_of_passes, data)

# result.to_csv("HQPass_nwhl.csv", index = True)


# result = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\HQPass_nwhl.csv")

# Overall Baseline for HQ Passing - 'scouting' dataset
# scouting_BL_HQP = result.groupby("HQ_Pass").count()/len(result)
# print("'scouting' dataset baseline HQ Pass: " + str(round(scouting_BL_HQP.loc['Yes', 'game_date'] * 100, 2)))

# For each team, Baseline for HQ Passing - 'scouting' dataset
# teams = list(set(result['Team']))

# for team in teams:
#     team_df = result.loc[result['Team'] == team, :]
#     team_BL_HQP = team_df.groupby("HQ_Pass").count() / len(team_df)
#     print(team + " baseline HQ Pass: " + str(round(team_BL_HQP.loc['Yes', 'game_date'] * 100, 2)) + "%")

# Logistic Regression on 'scouting' dataset, filtered for  for HDP as a function of:

lr_df = result.loc[result['Manpower'] == 'Even', ('Detail_1', 'Game_State', 'HQ_Pass', 'secLastAnyEvent', 'Period', 'euc_dist', 'Game_State', 'Team')]
lr_df = pd.get_dummies(lr_df, columns=['Detail_1', 'Game_State', 'Game_State', 'Period', 'Team'])

X = lr_df.drop(columns = 'HQ_Pass')

cleanup_HQP = {"HQ_Pass": {"Yes": 1, "No": 0}}
lr_df = lr_df.replace(cleanup_HQP)
y = lr_df.loc[:,'HQ_Pass']

# Split into test/train sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=1)

clf = LogisticRegression(random_state=0).fit(X_train, y_train)
clf.predict(X_test)
clf.predict_proba(X_test)
print(clf.score(X_test, y_test))

print(OLS(y_test, X_test).fit().summary())