from collections import defaultdict

import numpy as np


def transform_coordinate(coordinate, limit_from, limit_to):
    return (coordinate * limit_to) / limit_from


def get_player_positions(events, team_id, players_df, only_event=None, 
                         coordinate_system_from=(100,100), 
                         coordinate_system_to=(100,100), team_lineup=None):
    """
    Compute the average position of players on the pitch. If only_event
    is given only this type of events are considered in the computation. 
    Based on
    https://colab.research.google.com/github/devinpleuler/analytics-handbook/blob/master/notebooks/data_visualization.ipynb
    """

    positions = {}
    for e in events:
        if e['teamId'] == team_id and (not only_event or (only_event and e['eventName'] == only_event)):
            if not team_lineup or (team_lineup and int(e['playerId']) in team_lineup.keys()):
                player = players_df.loc[int(e['playerId'])]['shortName']
                if player not in positions.keys():
                    positions[player] = {'x':[], 'y':[]}
                if 'positions' in e.keys():
                    x, y = e['positions'][0]['x'], e['positions'][0]['y']
                    positions[player]['x'].append(x)
                    positions[player]['y'].append(y)
    avg_positions = {k:[np.mean(v['x']), np.mean(v['y'])] for k, v in positions.items()}
    return avg_positions


def get_passes_by_players(events, team_id, players_df):
    passes_by_players = defaultdict(int)
    for e in events:
        if e['eventName'] == 'Pass' and e['teamId'] == team_id:
            player_id = e['playerId']
            player = players_df.loc[int(player_id)]['shortName']
            passes_by_players[player] += 1
    return passes_by_players
