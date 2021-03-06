import pandas as pd

data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_scouting_amended.csv")
all_passes = data.loc[(data['Event'] == 'Play') | (data['Event'] == 'Incomplete Play')]

def helper_passDirection(origin_X, dest_X):
    delta_X = dest_X - origin_X
    if delta_X < -5:
        state = "Back"
    elif delta_X > 5:
        state = "Forward"
    else:
        state = "Neutral"

    return state

all_passes['passDirection'] = all_passes.apply(lambda row: helper_passDirection(row['X_Coordinate'], row['X_Coordinate_2']), axis=1)

# Create pairID and coordinates for drawing passes
coor_df = pd.DataFrame(columns=['pairID', 'game_date', 'Player', 'Event', 'X', 'Y', 'Team', 'Manpower', 'Type', 'State', 'sec_Control', 'passDirection'])
for index, row in all_passes.head(2000).iterrows():
    coor_df = coor_df.append({'pairID': str(row['game_date']) + "-" + str(row['event_id']), 'game_date': row['game_date'], 'Player': row['Player'], 'Event': row['Event'], 'X': row['X_Coordinate'], 'Y': row['Y_Coordinate'], 'Team': row['Team'], 'Manpower': row['Manpower'], 'Type': row['Detail_1'], 'State': row['Game_State'], 'sec_Control': row['secLastAnyEvent'], 'passDirection': row['passDirection']}, ignore_index=True)
    coor_df = coor_df.append({'pairID': str(row['game_date']) + "-" + str(row['event_id']), 'game_date': row['game_date'], 'Player': row['Player'], 'Event': row['Event'], 'X': row['X_Coordinate_2'], 'Y': row['Y_Coordinate_2'], 'Team': row['Team'], 'Manpower': row['Manpower'], 'Type': row['Detail_1'], 'State': row['Game_State'], 'sec_Control': row['secLastAnyEvent'], 'passDirection': row['passDirection']}, ignore_index=True)

coor_df.to_csv("hackathon_scouting_all_passes.csv")