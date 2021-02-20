import pandas as pd
import numpy as np

data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_womens_amended.csv")

# Helper Functions
# Filter for a specific team
def filter_by_team(teamname, df):
    return df.loc[df['Team'] == teamname,]

# Generate a baseline for passing
PASSES = data.loc[(data['Event'] == 'Play') | (data['Event'] == 'Incomplete Play'),]

# Analyze based on game state
PASSES = PASSES.loc[PASSES['Game_State'] == 'Close Lead']

# Define various subsets
DIRECT_PASSES = PASSES.loc[PASSES['Detail_1'] == 'Direct']
INDIRECT_PASSES = PASSES.loc[PASSES['Detail_1'] == 'Indirect']
COMPLETE_PASSES = PASSES.loc[PASSES['Event'] == 'Play']
INCOMPLETE_PASSES = PASSES.loc[PASSES['Event'] == 'Incomplete Play']

# Baseline successful passes, all inclusive
bl_scs_pass = round(len(COMPLETE_PASSES) / len(PASSES), 2)
print("Baseline Successful Passes: " + str(bl_scs_pass))

# Baseline passing by Direct/Indirect and Complete/Incomplete
pct_pass_direct = round(len(DIRECT_PASSES) / len(PASSES), 2)
print("Percentage of passes that are 'Direct': " + str(pct_pass_direct))
pct_pass_indirect = round(len(INDIRECT_PASSES) / len(PASSES), 2)
print("Percentage of passes that are 'Indirect': " + str(pct_pass_indirect))
pct_scs_pass_direct = round(len(pd.merge(DIRECT_PASSES, COMPLETE_PASSES, how='inner')) / len(DIRECT_PASSES), 2)
print("Percentage of successful passes that are 'Direct': " + str(pct_scs_pass_direct))
pct_scs_pass_indirect = round(len(pd.merge(INDIRECT_PASSES, COMPLETE_PASSES, how='inner')) / len(INDIRECT_PASSES), 2)
print("Percentage of successful passes that are 'Indirect': " + str(pct_scs_pass_indirect))

# Visualization Section
import matplotlib.pyplot as plot

def compare_plots(dist1, dist2, bin_list):
    ax[0, 0].hist(dist1['euc_dist'], bins=bin_list)
    ax[0, 1].hist(dist2['euc_dist'], bins=bin_list)
    ax[0, 0].title.set_text('dist1')
    ax[0, 1].title.set_text('dist2')

    ax[1, 0].hist(dist1['std_X_2'] - dist1['std_X'], bins=bin_list)
    ax[1, 1].hist(dist2['std_X_2'] - dist2['std_X'], bins=bin_list)
    ax[1, 0].title.set_text('dist1 (X)')
    ax[1, 1].title.set_text('dist2 (X)')

    ax[2, 0].hist(dist1['std_Y_2'] - dist1['std_Y'], bins=bin_list)
    ax[2, 1].hist(dist2['std_Y_2'] - dist2['std_Y'], bins=bin_list)
    ax[2, 0].title.set_text('dist1 (Y)')
    ax[2, 1].title.set_text('dist2 (Y)')

    plot.show()

    return

# Prepare a plot space
fig, ax = plot.subplots(3, 2)

# Calculate Euclidean Distance from pass origin to pass destination
pass_type = COMPLETE_PASSES
team_name = 'Olympic (Women) - Canada'
analysis = filter_by_team(team_name, pass_type)

compare_plots(pass_type, analysis, range(0, 200, 5))

