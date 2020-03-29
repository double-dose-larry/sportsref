from .br_page import BaseballPage
from ..util import *
from .team_season import TeamSeason

all_fran_df = get_players_or_teams('baseball', 'team')

class Franchise():
    
    def __init__(self, fuzzy_fran):
        f = find_player_or_team(fuzzy_fran, all_fran_df)
        self.abbr = f.abbr
        self.name = f.name
        self.first_year = int(f.years[:4])
        self.last_year = int(f.years[-4:])
        self.years_active = list(range(self.first_year, self.last_year + 1))
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year} >"
    
    def hist(self):
        path = f"teams/{self.abbr}"
        return BaseballPage(path)

    def people_pages(self, page=""):
        validate_input(page, ["pitch", "bat", "managers", "opening",
                                     "pos", "staff"])
        path = f"teams/{self.abbr}/{people_type}.shtml"
        return BaseballPage(path)

    
    def year_by_year_pages(self, page=""):
        validate_input(page, ["pitch", "bat"])
        path = f"teams/{self.abbr}/{pit_or_bat}team.shtml"
        return BaseballPage(path)
    
    def honors_pages(self, page=""):
        validate_input(page, ["pitch-all-star", "bat-all-star", "hof"])        
        path = f"teams/{self.abbr}/{honors_type}.shtml"
        return BaseballPage(path)

    # these is from the 'Other' menu
    def draft(self, year):
        path = "/draft"
        query_dict = {
            'team': self.abbr,
            'year_ID': year,
            'draft_type' : 'junreg',
            'query_type' : 'franch_year',
            'from_type_jc' : 0,
            'from_type_hs' : 0,
            'from_type_4y' : 0,
            'from_type_unk' : 0
        }
        return BaseballPage(path, query_dict)
    
    def parks(self):
        path = f'teams/{self.abbr}/attend.shtml'
        return BaseballPage(path)
    
    # this is will return a TeamSeason object that will have it's own pages
    def season(self, year):
        validate_input(year, self.years_active)
        return TeamSeason(self, year)