from .pfr_page import PFRPage
from .util import *

all_player_df = get_players()

class Player():
    
    def __init__(self, fuzzy_name):
        p = get_player_info(fuzzy_name, all_player_df, verbose=True)
        self.key = p.key
        self.name = p["name"]
        self.first_year = int(p.years[:4])
        self.last_year = int(p.years[-4:])
        self.is_active = p.is_active == 1
        self.years_active = list(range(self.first_year, self.last_year + 1))

        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year}, {'active' if self.is_active else 'not active'} >"
        
    def overview(self):
        # get player overview page
        path = f"/players/{self.key[0]}/{self.key}.htm"
        return PFRPage(path)
    
    def gamelogs_pages(self, year):
        validate_input(year, self.years_active + ["career", "post"])
        if year == 'career':
            year = ''
        path = f"players/{self.key[0]}/{self.key}/gamelog/{year}"
        return PFRPage(path)
    
    def splits_pages(self, year):
        validate_input(year, self.years_active + ["career"])
        if year == 'career':
            year = ''
        path = f"players/{self.key[0]}/{self.key}/splits/{year}"
        return PFRPage(path)
    
    def plays_pages(self, year, play_type):
        validate_input(year, self.years_active)
        validate_input(play_type, ['receiving', 'passing', 'rushing'])
        path = f"players/{self.key[0]}/{self.key}/{play_type}-plays/{year}"
        return PFRPage(path)
    
    def more_pages(self, page="penalties"):
        validate_input(page, ["penalties"])
        path = f"players/{self.key[0]}/{self.key}/penalties"
        return PFRPage(path)