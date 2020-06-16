from .pfr_page import ProFootballPage
from ..util import *

all_fran_df = get_players_or_teams('football', 'team')

class Franchise():
    
    def __init__(self, fuzzy_fran):
        f = find_player_or_team(fuzzy_fran, all_fran_df)
        print(f)
        self.abbr = f.abbr
        self.name = f.name
        self.first_year = int(f.years[:4])
        self.last_year = int(f.years[-4:])
        self.years_active = list(range(self.first_year, self.last_year + 1))
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year} >"

    def hist(self):
        path = f"teams/{self.abbr}"
        return ProFootballPage(path)