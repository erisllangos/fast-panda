import sys
sys.path.insert(0, '../src')
from season_schedule import *
get_season_schedule(2008).head()
print(get_season_schedule(2019).head())
print(get_season_schedule('2008').head())
get_season_schedule('notasite')
