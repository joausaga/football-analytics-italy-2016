

def generate_pass_network(events, team_id, players_df):
    """
    Generate the network of the passes of the team given by team_id. Based on 
    https://github.com/Friends-of-Tracking-Data-FoTD/mapping-match-events-in-Python/blob/master/data_exploration.ipynb
    and
    https://colab.research.google.com/github/devinpleuler/analytics-handbook/blob/master/notebooks/data_visualization.ipynb
    """

    ACCURATE_PASS = 1801
    team_passes = {}
    for event, next_event, next_next_event in zip(events, events[1:], events[2:]):
        passer, receiver = None, None
        try:
            if event['eventName'] == 'Pass' and event['teamId'] == team_id and \
               ACCURATE_PASS in [tag['id'] for tag in event['tags']]:
                passer = players_df.loc[int(event['playerId'])]['shortName']
                # case of duel
                if next_event['eventName'] == 'Duel':
                    # if the next event of from a player of the same team
                    if next_event['teamId'] == event['teamId']:
                        receiver = players_df.loc[int(next_event['playerId'])]['shortName']
                    else:
                        receiver = players_df.loc[int(next_next_event['playerId'])]['shortName']
                # any other event 
                else:
                    if next_event['teamId'] == event['teamId']:
                        receiver = players_df.loc[int(next_event['playerId'])]['shortName']
                if passer and receiver and passer != receiver: # avoid auto-passes
                    a, b = sorted([passer, receiver])
                    if a not in team_passes.keys():
                        team_passes[a] = {}
                    if b not in team_passes[a].keys():
                        team_passes[a][b] = 0
                    team_passes[a][b] += 1
        except KeyError as e:
            print(f'Error {e}')
    
    return team_passes

def compute_pass_lines(passes, positions, min_num_passes=None, team_lineup=None):
    lines = []
    weights = []
    for k, v in passes.items():
        if not team_lineup or (team_lineup and k in team_lineup.values()):
            origin = positions[k]
            for k_, v_ in passes[k].items():
                if not team_lineup or (team_lineup and k_ in team_lineup.values()):
                    if not min_num_passes or (min_num_passes and v_ >= min_num_passes):
                        dest = positions[k_]
                        lines.append([*origin, *dest])
                        weights.append(v_)
    return lines, weights