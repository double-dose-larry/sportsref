import pandas as pd
from fuzzywuzzy import process


def validate_input(inpt, valid_choices):
    if not inpt in valid_choices:
        raise Exception(f"error with choice {inpt}. valid choices are {valid_choices}")

def get_players_or_teams(sport, player_or_team):
    validate_input(sport, ["baseball", "football", "basketball", "hockey", "soccer"])
    validate_input(player_or_team, ["player", "team", "club"])
    if sport == 'soccer' and player_or_team == 'team':
        player_or_team == 'club'
        
    cdn = {
    'baseball' : 'd3k2oh6evki4b7',
    'football' : 'd395i9ljze9h3x',
    'basketball' : 'd2cwpp38twqe55',
    'hockey' : 'd9kjk42l7bfqz',
    'soccer': 'd6rt22vwfyr3i'
    }.get(sport)
    
    csv_url = f"https://{cdn}.cloudfront.net/short/inc/{player_or_team}s_search_list.csv"
    if player_or_team == 'player':
        csv_df = (pd.read_csv(csv_url,
                      names=["key", "name", "years", "is_active", 
                             "country", "country_short", "team_list", "_columns", "pop_rank"])
                      .dropna(thresh=1000, axis=1) # drop empty columns
                     ).sort_values("pop_rank", ascending=False) # put the most popular searches up top
    else:
        csv_df = (pd.read_csv(csv_url,
                      names=["abbr", "name", "years", "0", "1", "2", "3", "4", "5"])
          .dropna(axis=1) # drop empty columns
          .drop("0", axis =1) # drop 0 column
         )
    return csv_df

def find_player_or_team(search_string, search_df, indx=0, verbose=False):
    name, pct_sure, index = process.extract(search_string, search_df.name, limit=3)[indx]
    if verbose:
        print(f"I'm {pct_sure}% sure that you want {name}")
    return search_df.loc[index]