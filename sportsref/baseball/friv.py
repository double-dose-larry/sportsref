from .br_page import BaseballPage
from ..util import *

class Frivolities():
       
    def bio_state(self, state=""):
#         validate_input(page, ["bat", "pitch", "manage"])
        path = f"bio/{state}_born.shtml"
        return BaseballPage(path)