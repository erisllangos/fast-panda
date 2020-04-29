import pandas as pd
import requests
import io
import json


def get_season_schedule(season):
    if type(season) == int: season = str(season)
    
    url = "http://www.nfl.com/feeds-rs/schedules/"+season
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Looks like you have an error;", err)
        return
    
    #this check will be removed once xml gets read in for prior szns
    if int(season) < 2000:
        print("Sorry no data for seasons prior to 2000")
        return
    
    df=pd.read_json(io.StringIO(resp.content.decode('UTF-8')))
    df=df['gameSchedules'].apply(pd.Series)
    
    if df.empty:
        print("Please put in a valid season. 2000-2019")
        return
    
    return df
