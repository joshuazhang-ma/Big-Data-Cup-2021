import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

idx = pd.IndexSlice

data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_scouting_amended.csv")

multi = data.set_index(['game_date', 'Period', 'Game_State', 'Manpower', 'Event', 'Detail_1', 'Team', 'Player']).sort_index()

# Constants
teams = list(set(data['Team']))

# Helper Functions

def calc_vif(X):

    # Calculating VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

    return(vif)

def passDirection(df):
    df.loc[df['X_Coordinate'] - df['X_Coordinate_2'] < -5, 'passDir'] = 'Back'
    df.loc[(df['X_Coordinate'] - df['X_Coordinate_2'] >= -5) & (df['X_Coordinate'] - df['X_Coordinate_2'] <= 5), 'passDir'] = 'Sideways'
    df.loc[df['X_Coordinate'] - df['X_Coordinate_2'] > 5, 'passDir'] = 'Forward'

    return df

def passOriginZone(df):
    df.loc[df['X_Coordinate'] < 75, 'passZone'] = 'D'
    df.loc[(df['X_Coordinate'] >= 75) & (df['X_Coordinate'] <= 125), 'passZone'] = 'N'
    df.loc[df['X_Coordinate'] > 125, 'passZone'] = 'O'

    return df

# Filter for a specific team
def filter_by(column_name, value, df):
    try:
        return df.loc[df[column_name] == value,]
    except:
        print("Error in filter, returning original dataframe.")
        return df

def compare_dist_plots(baseline, dist2, teamname, bins=range(0, 200, 10)):
    fig, ax = plt.subplots(2, 3)
    row_names = ['Baseline', teamname]

    ax[0, 0].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['euc_dist'], bins, alpha=0.5, label='Play')
    ax[0, 0].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['euc_dist'], bins, alpha=0.5, label='Incomplete Play')

    ax[1, 0].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)),:]['euc_dist'], bins, alpha=0.5, label='Play')
    ax[1, 0].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['euc_dist'], bins, alpha=0.5, label='Incomplete Play')
    ax[0, 0].title.set_text('Euclidean')
    ax[1, 0].title.set_text('Euclidean')

    ax[0, 1].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_X_2'] -
                  baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_X'], bins, alpha=0.5, label='Play')
    ax[0, 1].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_X_2'] -
                  baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_X'], bins, alpha=0.5, label='Incomplete Play')

    ax[1, 1].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_X_2'] -
                  dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_X'], bins, alpha=0.5, label='Play')
    ax[1, 1].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_X_2'] -
                  dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_X'], bins, alpha=0.5, label='Incomplete Play')

    ax[0, 1].title.set_text('(X)')
    ax[1, 1].title.set_text('(X)')

    ax[0, 2].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_Y_2'] -
                  baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_Y'], bins, alpha=0.5, label='Play')
    ax[0, 2].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_Y_2'] -
                  baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_Y'], bins, alpha=0.5, label='Incomplete Play')

    ax[1, 2].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_Y_2'] -
                  dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['std_Y'], bins, alpha=0.5, label='Play')
    ax[1, 2].hist(dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_Y_2'] -
                  dist2.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['std_Y'], bins, alpha=0.5, label='Incomplete Play')
    ax[0, 2].title.set_text('(Y)')
    ax[1, 2].title.set_text('(Y)')

    for ax_t, row in zip(ax[:, 0], row_names):
        ax_t.set_ylabel(row, rotation=90, size='large')

    fig.suptitle('Passing Distance, in feet', fontsize=16)
    fig.tight_layout()
    plt.show()

    return

def compare_pass_type_plots(baseline, df, teamname, bins=range(0, 10, 1)):
    fig, ax = plt.subplots(2, 3)

    ax[0][0].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)),:]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[0][0].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[0, 0].title.set_text('Baseline - Pass')
    ax[1][0].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', slice(None), slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[1][0].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', slice(None), slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[1, 0].title.set_text(teamname + ' - Pass')

    ax[0][1].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Direct', slice(None), slice(None)),:]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[0][1].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Direct', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[0, 1].title.set_text('Baseline - Direct Pass')
    ax[1][1].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Direct', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[1][1].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Direct', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[1, 1].title.set_text(teamname + ' - Direct Pass')

    ax[0][2].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Indirect', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[0][2].hist(baseline.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Indirect',slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[0, 2].title.set_text('Baseline - Indirect Pass')
    ax[1][2].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Indirect', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Play')
    ax[1][2].hist(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Indirect', slice(None), slice(None)), :]['secLastAnyEvent'], bins, alpha=0.5, label='Incomplete Play')
    ax[1, 2].title.set_text(teamname + ' - Indirect Pass')

    plt.show()

    return

def get_asterisks_for_pval(p_val):
    """Receives the p-value and returns asterisks string."""
    if p_val > 0.05:
        p_text = "ns"  # above threshold => not significant
    elif p_val < 1e-4:
        p_text = '****'
    elif p_val < 1e-3:
        p_text = '***'
    elif p_val < 1e-2:
        p_text = '**'
    else:
        p_text = '*'

    return p_text

def perform_cs_test(teams, df):
    chitest_matrix = pd.DataFrame(columns=['Team', 'p_dir', 'p_indir', 'ip_dir', 'ip_indir'])

    # Add baseline
    play_direct = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Direct', slice(None), slice(None)), :])
    play_indirect = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Indirect', slice(None), slice(None)), :])
    incplay_direct = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Direct', slice(None), slice(None)), :])
    incplay_indirect = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Indirect', slice(None), slice(None)), :])

    new_row = {'Team': 'Baseline', 'p_dir': play_direct, 'p_indir': play_indirect, 'ip_dir': incplay_direct, 'ip_indir': incplay_indirect}
    chitest_matrix = chitest_matrix.append(new_row, ignore_index=True)

    for team in teams:
        play_direct = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Direct', team, slice(None)), :])
        play_indirect = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Play', 'Indirect', team, slice(None)), :])
        incplay_direct = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Direct', team, slice(None)), :])
        incplay_indirect = len(df.loc[(slice(None), slice(None), slice(None), slice(None), 'Incomplete Play', 'Indirect', team, slice(None)), :])

        new_row = {'Team': team, 'p_dir': play_direct, 'p_indir': play_indirect, 'ip_dir': incplay_direct, 'ip_indir': incplay_indirect}
        chitest_matrix = chitest_matrix.append(new_row, ignore_index=True)

    chitest_matrix = chitest_matrix.set_index('Team')
    stat, p, dof, expected = chi2_contingency(chitest_matrix)

    # interpret p-value
    alpha = 0.05
    print("p value is " + str(p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (H0 holds true)')

    # Pairwise chi-squared test with printout
    from itertools import combinations

    # gathering all combinations for post-hoc chi2
    all_combinations = list(combinations(chitest_matrix.index, 2))
    p_vals = []

    for comb in all_combinations:
        # subset df into a dataframe containing only the pair "comb"
        new_df = chitest_matrix[(chitest_matrix.index == comb[0]) | (chitest_matrix.index == comb[1])]
        # running chi2 test
        chi2, p, dof, ex = chi2_contingency(new_df, correction=True)
        p_vals.append(p)

        from statsmodels.sandbox.stats.multicomp import multipletests

        reject_list, corrected_p_vals = multipletests(p_vals, method='fdr_bh')[:2]

        print("original p-value\tcorrected p-value\treject?")
        for p_val, corr_p_val, reject, comb in zip(p_vals, corrected_p_vals, reject_list, all_combinations):
            print(
                f"{comb}: p_value: {p_val:5f}; corrected: {corr_p_val:5f} ({get_asterisks_for_pval(p_val)}) reject: {reject}")

    return

def eventAfterTurnover(df):
    inc_pass_index = df.index[df['Event'] == 'Incomplete Play'].tolist()
    try:
        inc_pass_index.remove(len(df)-1)
    except:
        print("")

    # For all zones, Turnover
    next_event_index = [x + 1 for x in inc_pass_index if df.iloc[x + 1,]['TeamIdentity'] != df.iloc[x,]['TeamIdentity']]

    next_event = df.iloc[next_event_index,]
    print("For all zones: ")
    print(next_event.groupby(['TeamIdentity', 'Event'])['Event'].count())

    # For Turnovers originating from a defensive zone
    next_event_def_index = [x + 1 for x in inc_pass_index if (df.iloc[x + 1,]['TeamIdentity'] != df.iloc[x,]['TeamIdentity']) & (df.iloc[x,]['passZone'] == 'D')]

    next_def_event = df.iloc[next_event_def_index,]
    print("For defensive zone turnovers: ")
    print(next_def_event.groupby(['TeamIdentity', 'Event'])['Event'].count())

    # For Turnovers originating from the neutral zone
    next_event_neu_index = [x + 1 for x in inc_pass_index if
                            (df.iloc[x + 1,]['TeamIdentity'] != df.iloc[x,]['TeamIdentity']) & (
                                        df.iloc[x,]['passZone'] == 'N')]

    next_neu_event = df.iloc[next_event_neu_index,]
    print("For neutral zone turnovers: ")
    print(next_neu_event.groupby(['TeamIdentity', 'Event'])['Event'].count())

    # For Turnovers originating from an offensive zone
    next_event_off_index = [x + 1 for x in inc_pass_index if df.iloc[x,]['passZone'] == 'O']

    next_off_event = df.iloc[next_event_off_index,]
    print("For offensive zone turnovers: ")
    print(next_off_event.groupby(['TeamIdentity', 'Event'])['Event'].count())

    return

# Get indexes of all incomplete plays
def catch(func, handle=lambda e : e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle(e)

### Given a game, graph passing success rates:
## By score state
data = data.loc[(data['Event'] == 'Play') | (data['Event'] == 'Incomplete Play')]

### Transform categorical to numeric for MC check below
data = pd.get_dummies(data, columns=['Detail_1', 'Game_State', 'Manpower'])

data = data.drop(['event_id', 'Home_Team_Skaters', 'Away_Team_Skaters', 'std_X', 'std_X_2', 'std_Y', 'std_Y_2', 'X_Coordinate_2', 'Y_Coordinate_2', 'Period'], axis=1)

# corrMatrix = data.corr()
# sn.heatmap(corrMatrix, annot=True)
# plt.show()

# Detecting and Fixing Multicollinearity
# X = data.select_dtypes('number').iloc[:,:-1]
# print(calc_vif(X))

### Perform Logistic Regression

X = data.loc[:, ['']]
y = data.loc[:, 'Event']
print(X.head(5))
print(y.head(5))

clf = LogisticRegression(random_state=0).fit(X, y)
clf.predict(X[:2, :])
clf.predict_proba(X[:2, :])
clf.score(X, y)