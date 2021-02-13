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

def home_away(data, df_index):
    record = data[df_index,]
    event_owner = record['Team']
    home_team = record['Home Team']
    if(event_owner == home_team):
        state = "Home"
    else:
        state = "Away"

    return state

def cate_zone(x_coor, team_for_against):
    if team_for_against=="for":
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

def side_zone(y_coor, team_for_against):


    return categorization

def std_coor(data, x_coor, y_coor, team_name):
    # Given the dataset, it makes more sense to orient all coordinates to the POV of the team in analysis
    data['std_X'] = data['X Coordinate']
    data['std_X'] = [200-]

    return x, y

def manpower_state(for_players, against_players):
    if for_players > against_players:
        state = "Advantage"
    elif for_players < against_players:
        state = "Shorthanded"
    else:
        state = "Even"

    return state

def score_state(for_score, against_score):
    if for_score - against_score <= -2:
        state = "Trail"
    elif for_score - against_score == -1:
        state = "Close Trail"
    elif for_score - against_score >= 2:
        state = "Lead"
    elif for_score - against_score == 1:
        state = "Close Lead"
    else:
        state = "Even"

    return state

def initiation():
    data = pd.read_csv("C:\\Users\\CLZ\\Documents\\GitHub\\Big-Data-Cup-2021\\hackathon_womens.csv")

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
        home_team = group.iloc[1]["Home Team"]
        away_team = group.iloc[1]["Away Team"]

        # how many zone entry events in a game
        cnt_zone_entry = group.loc[group["Event"] == "Zone Entry", ]["Event"].count()
        for name, group in

        print(cnt_zone_entry)

    return

def main():
    data = initiation()
    print(data.head(10))

    zoneEntry(data)

    return

main()