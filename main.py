import pandas as pd
import os

#### CONSTANTS
MIN_X = 0
MAX_X = 200
MIN_Y = 0
MAX_Y = 85

CENTER_X = 100
FO_DEF_X = 31
FO_N_DEF_X = 80
FO_N_OFF_X = 120
FO_OFF_X = 169
CENTER_Y = [42, 43]
LW_Y = [20, 21]
RW_Y = [64, 65]

ZN_DEF_X = 75
ZN_OFF_X = 125

# Variables #####
data = None

# Data Wrangling Functions #####

def cate_zone(x_coor, team_identity, period):
    if (team_identity=="Home Team" and period != 2) or (team_identity=="Away Team" and period == 2):
        if x_coor < 75:
            categorization = "Defensive Zone"
        elif x_coor < 125:
            categorization = "Neutral Zone"
        else:
            categorization = "Offensive Zone"
    else:
        if x_coor < 75:
            categorization = "Offensive Zone"
        elif x_coor < 125:
            categorization = "Neutral Zone"
        else:
            categorization = "Defensive Zone"

    return categorization

def side_zone(y_coor, team_identity, period):
    if (team_identity=="Home Team" and period != 2) or (team_identity=="Away Team" and period == 2):
        if y_coor <= 20:
            categorization = "Left Wing"
        elif y_coor >= 65:
            categorization = "Right Wing"
        else:
            categorization = "Mid-Ice"
    else:
        if y_coor <= 20:
            categorization = "Offensive Zone"
        elif y_coor < 125:
            categorization = "Neutral Zone"
        else:
            categorization = "Defensive Zone"

    return categorization

def std_coor(data):
    # Given the dataset, it makes more sense to orient all coordinates to the POV of the home team
    data['std_X'] = data['X_Coordinate']
    data['std_X_2'] = data['X_Coordinate_2']
    # data['std_X'] = [200 - data.iloc[row]['X Coordinate'] for row in data if data['Team Identity'] == "Away Team"]
    data.loc[data['TeamIdentity'] == "Away Team", 'std_X'] = 200 - data['X_Coordinate']
    data.loc[data['TeamIdentity'] == "Away Team", 'std_X_2'] = 200 - data['X_Coordinate_2']

    data['std_Y'] = data['Y_Coordinate']
    data['std_Y_2'] = data['Y_Coordinate_2']
    # data['std_Y'] = [85 - data.iloc[row]['Y Coordinate'] for row in data if data['Team Identity'] == "Away Team"]
    data.loc[data['TeamIdentity'] == "Away Team", 'std_Y'] = 85 - data['Y_Coordinate']
    data.loc[data['TeamIdentity'] == "Away Team", 'std_Y_2'] = 85 - data['Y_Coordinate_2']

    return data

def cte_id(data):
    # Old way, simple but effective, does not reset id for each new game. Cannot help with calculating time elapsed team event
    data['event_id'] = data.index + 1
    group_data = data.groupby('game_date')
    for name, group in group_data:
        group = group.reset_index()
        group['event_id'] = group.index + 1

    return data

def cte_team_identity(data):
    data['TeamIdentity'] = data['Team']

    data.loc[data['Team'] == data['Home_Team'], 'TeamIdentity'] = "Home Team"
    data.loc[data['Team'] == data['Away_Team'], 'TeamIdentity'] = "Away Team"

    return data

def cte_score_diff(data):
    data['Score_Differential'] = 0
    data.loc[data['TeamIdentity'] == 'Home Team', 'Score_Differential'] = data['Home_Team_Goals'] - data['Away_Team_Goals']
    data.loc[data['TeamIdentity'] == 'Away Team', 'Score_Differential'] = data['Away_Team_Goals'] - data['Home_Team_Goals']

    data['Game_State'] = [score_state(value) for value in data['Score_Differential']]

    return data

def cte_time_remaining(data):
    data['Time_Remaining'] = [int(x.split(":")[0])*60 + int(x.split(":")[1]) for x in data['Clock']]

    return data

def cte_timeElapsed_team_event(data):
    data['secLastEvent'] = data.apply(lambda row: helper_cte_timeElapsed_team_event(row['Time_Remaining'], row['Period'], row['game_date'], row['TeamIdentity'], row['event_id'], data), axis=1)

    return data

def helper_cte_timeElapsed_team_event(event_time, event_period, event_game_date, team_identity, event_id, data):
    try:
        period_data = data.loc[(data['game_date'] == event_game_date) & (data['Period'] == event_period) & (data['TeamIdentity'] == team_identity) & (data['event_id'] < event_id),]
        prev_event_time = period_data.iloc[-1]['Time_Remaining']
    except:
        return -1

    return prev_event_time - event_time

def cte_manpower(data):
    data['Manpower'] = data.apply(lambda row: helper_manpower_state(row['Home_Team_Skaters'], row['Away_Team_Skaters']), axis=1)

    return data

def helper_manpower_state(for_players, against_players):
    if for_players > against_players:
        state = "Advantage"
    elif for_players < against_players:
        state = "Shorthanded"
    else:
        state = "Even"

    return state

def score_state(Score_Differential):
    if Score_Differential <= -2:
        state = "Trail"
    elif Score_Differential == -1:
        state = "Close Trail"
    elif Score_Differential >= 2:
        state = "Lead"
    elif Score_Differential == 1:
        state = "Close Lead"
    else:
        state = "Tied"

    return state

# Analysis Functions #####

def initiation():
    data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_womens.csv")
    data.columns = data.columns.str.replace(" ", "_")

    # Reduced data rows for testing purposes.
    # data = data.iloc[0:50]

    data = cte_time_remaining(data)
    data = cte_id(data)
    data = cte_team_identity(data)
    data = std_coor(data)
    data = cte_score_diff(data)
    data = cte_timeElapsed_team_event(data)
    data = cte_manpower(data)

    # define method of zone entry

    ### The categorization already exists in the provided dataset.

    # categorize zone of coordinates of an event


    return data

# Return series of events from acquiring posession to zone entry
def slc_zoneEntry(data):
    POSITIVE_SAME_TEAM = ["Shot", "Goal", "Play", "Puck Recovery"]
    NEGATIVE_SAME_TEAM = ["Incomplete Play", "Penalty Taken"]

    # Zone Entries

    # Overall Zone Entry Success Rate - A successful zone entry includes any zone entry where the attacking team retains possession and makes one more possession play (e.g. Shot, Pass, Goal)
    idx_initial = 0 # Event_id of zone entry
    idx_next = 0 # Event_id of next entry

    grouped = data.groupby("game_date")
    for name, group in grouped:
        home_team = group.iloc[1]["Home_Team"]
        away_team = group.iloc[1]["Away_Team"]

        # how many zone entry events in a game
        cnt_zone_entry = group.loc[group["Event"] == "Zone Entry", ]["Event"].count()
        # for name, group in

        print(cnt_zone_entry)

    return

# Return series of events between face-off to goal
def slc_scoringSequence(data):
    output_list = []
    # get list of indices of goals
    goal_indices = data.index[data['Event'] == 'Goal'].tolist()
    for index in goal_indices:
        events_list = get_slice(data, "Faceoff Win", index)
        all_events = events_list['Event']
        scoring_team_events = events_list.loc[events_list['Team'] == events_list[index]['Team']]['Event']
        output_list.append(list(events_list))
        output_df = pd.DataFrame(output_list)
        output_df.to_csv("scoring_sequence.csv")

    return

def get_slice(data, starting_event, ending_event_index):
    try:
        starting_event_index_list = data.index[data['Event'] == starting_event].tolist()
        starting_event_index = max(filter(lambda i: i < ending_event_index, starting_event_index_list))
    except:
        print("No slice found.")
        return pd.DataFrame()

    return data.iloc[starting_event_index:ending_event_index]

def main():
    # data = initiation()

    data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_womens_amended.csv")
    slc_scoringSequence(data)

    return

main()