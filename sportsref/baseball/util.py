import pandas as pd
from fuzzywuzzy import process
from urllib.parse import quote_plus

def get_players():
    player_db_url = "https://d3k2oh6evki4b7.cloudfront.net/short/inc/players_search_list.csv" # This is what baseball-reference puts in the browser to make their player search fast
#     print("im calling bref now")
    all_players_df = (pd.read_csv(player_db_url,
                      names=["key", "name", "years", "is_active", "_drop", "_these", "_empty", "_columns", "pop_rank"])
          .dropna(thresh=1000, axis=1) # drop empty columns
         ).sort_values("pop_rank", ascending=False) # put the most popular searches up top
    return all_players_df

def get_player_info(search_string, search_df, verbose=False):
    name, pct_sure, index = process.extract(search_string, search_df.name, limit=1)[0]
    if verbose:
        print(f"I'm {pct_sure}% sure that you want {name}")
    return search_df.loc[index]

def get_frans():
    url = "https://d3k2oh6evki4b7.cloudfront.net/short/inc/teams_search_list.csv"
    df = (pd.read_csv(url,
                      names=["abbr", "name", "years", "0", "1", "2", "3", "4", "5"])
          .dropna(axis=1) # drop empty columns
          .drop("0", axis =1) # drop 0 column
         )
    return df

def get_fran_info(df, search_string, verbose=True):
    name, pct_sure, index = process.extract(search_string, df.name.append(df.abbr), limit=1)[0]
    if verbose:
        print(f"I'm {pct_sure}% that you want {name}")
    return df.loc[index]
    

def validate_input(inpt, valid_choices):
    """
    raise an error if inpt is not in valid choices, this serves as a quick hint to the user
    """
    if not inpt in valid_choices:
        raise Exception(f"error with choice {inpt}. valid choices are {valid_choices}")

def ba(row):
    return row.H/row.AB

def obp(row):
    return (row.H + row.BB + row.HPB)/(row.AB + row.BB + row.HBP + row.SF)

def slg(row):
    singles = row.H - (row["2B"] + row["3B"] + row["HR"])
    return (singles + row["2B"] * 2 + row["3B"] * 3 + row["HR"] * 4)/row.AB
