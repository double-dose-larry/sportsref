import pandas as pd
from fuzzywuzzy import process

def get_players():
    player_db_url = "https://d3k2oh6evki4b7.cloudfront.net/short/inc/players_search_list.csv" # This is what baseball-reference puts in the browser to make their player search fast
    all_players_df = (pd.read_csv(player_db_url,
                      names=["key", "name", "years", "is_active", "_drop", "_these", "_empty", "_columns", "pop_rank"])
          .dropna(thresh=1000, axis=1) # drop empty columns
         ).sort_values("pop_rank", ascending=False) # put the most popular searches up top
    return all_players_df

def get_player_info(search_string, verbose=False):
    df = get_players()
    name, pct_sure, index = process.extract(search_string, df.name, limit=1)[0]
    if verbose:
        print(f"I'm {pct_sure}% sure that you want {name}")
    return df.loc[index]

def get_frans():
    url = "https://d3k2oh6evki4b7.cloudfront.net/short/inc/teams_search_list.csv"
    df = (pd.read_csv(url,
                      names=["abbr", "name", "years", "0", "1", "2", "3", "4", "5"])
          .dropna(axis=1) # drop empty columns
          .drop("0", axis =1) # drop 0 column
         )
    return df

def get_fran_info(search_string, verbose=True):
    df = get_teams()
    name, pct_sure, index = process.extract(search_string, df.name.append(df.abbr), limit=1)[0]
    if verbose:
        print(f"I'm {pct_sure}% that you want {name}")
    return df.loc[index]

def validate_input(inpt, valid_choices):
        if not inpt in valid_choices:
            raise Exception(f"error with choice {inpt}. valid choices are {valid_choices}")
            
        