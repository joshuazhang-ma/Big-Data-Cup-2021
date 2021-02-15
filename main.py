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

#### Variables
data = None

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
    data['event_id'] = data.index + 1

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

def cte_timeElapsed_team_event(index, row, data):
    # Given a game, period, and team, calculate the amount of seconds since their last event.
    time = 0
    # First subset the data based on the game, period and team of the row
    

    return time

def manpower_state(for_players, against_players):
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

def initiation():
    data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_womens.csv")
    data.columns = data.columns.str.replace(" ", "_")

    data = cte_time_remaining(data)
    print(data.head(10))
    data = cte_id(data)
    print(data.head(10))
    data = cte_team_identity(data)
    data = std_coor(data)
    data = cte_score_diff(data)
    print(data.head(10))

    # convert time left to time remaining in seconds

    time_remaining = data['Clock']
    split_TR = time_remaining.str.split(":")
    data['Time Remaining'] = [int(x[0])*60+int(x[1]) for x in split_TR]

    # define method of zone entry

    ### The categorization already exists in the provided dataset.

    # categorize zone of coordinates of an event


    return data

def zoneEntry(data):
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

def main():
    data = initiation()

    zoneEntry(data)

    return

main()