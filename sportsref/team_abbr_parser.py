from html.parser import HTMLParser
import urllib.request

class TeamAbbrParser(HTMLParser):
    
    def __init__(self, team_url):
        super().__init__()
        self.team_year_abbr_map = {}
        self.team_url = team_url
        self.read_html()
        
    def read_html(self):
        with urllib.request.urlopen(self.team_url) as res:
            self.html = res.read()
        self.feed(str(self.html))
    
    def handle_starttag(self, tag, attrs):
#         print("Encountered a start tag:", tag)
        if tag == 'a':
            for attr in attrs:
                at, val = attr
                if isinstance(val, str) and 'teams' in val:
                    abbr, year = val.split("/")[-2:]
                    year = year.split(".")[0]
                    if year.isdigit():
                        self.team_year_abbr_map[int(year)] = abbr