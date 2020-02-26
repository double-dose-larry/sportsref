## sportsref

## Install

clone the repo then

```python
pip install .
```

## Usage

grab data from baseball-reference.com via a nice OOP interface.

Generally speaking, the idea is to allow to grab any table that is seen on baseball-reference.com as a clean pandas dataframe.
The objects are loosely based on the pages available for each type of "thing" on the website.

For example, for a player you'll see start with the "Overview" page that contains several tables, such as **Standard Batting** and **Player Value--Batting**. The Player object provides away to grab those tables like so:

```python
from sportsref.baseball import Player
jiman = Player("Ji-Man Choi")
# returns a pandas df of the "Standard Batting" table
display(jiman.overview("batting_standard")) 
# returns a pandas df of the "Player Value--Batting" table
display(jiman.overview("batting_value"))
```


        
        
