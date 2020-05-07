import pandas as pd
import requests
import io
import json


def get_season_schedule(season):

    """Returns a dataframe for any season

    Args:
        season (int or string) - the season schedule to be scraped

    Returns:
        pandas.Dataframe: the dataframe for the selected season
    """

    if type(season) == int: season = str(season)
    
    url = f"http://www.nfl.com/feeds-rs/schedules/{season}.json"
    headers={'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'HttpError with status code: { err.response.status_code}')
        # Return an empty dataframe
        return pd.DataFrame()
    
    return _prepare_schedule_df(resp.content)

def _prepare_schedule_df(schedule_response):
    
    """
    Private method to restructure the response object into the form we need

    Args:
        schedule_response (dict) - reponse json from the schedule request
    Returns:
        (pandas.Dataframe) - proper schedule representation
    """
    # Get array that is nested under gameSchedules
    raw_schedules = json.loads(schedule_response)['gameSchedules']
    schedules_rows = []

    for schedule in raw_schedules:
        try:
            schedules_rows.append({
                'season': schedule['season'],
                'alt_game_id': f"{schedule['season']}_{schedule['week']:02d}_{schedule['homeTeamAbbr']}_{schedule['visitorTeamAbbr']}",
                'game_date': schedule['isoTime'],
                'home_team': schedule['homeTeamAbbr'],
                'away_team': schedule['visitorTeamAbbr'],
                'home_team_name': schedule['homeDisplayName'],
                'away_team_name': schedule['visitorDisplayName'],
                'home_nickname': schedule['homeNickname'],
                'away_nickname': schedule['visitorNickname'],
                'home_team_id': schedule['homeTeamId'],
                'away_team_id': schedule['visitorTeamId'],
                'game_type': schedule['gameType'],
                'week_name': schedule['weekName'],
                'site_city': schedule['site']['siteCity'],
                'site_fullname': schedule['site']['siteFullname'],
                'site_state': schedule['site']['siteState'],
                'site_roof_type': schedule['site']['roofType']
            })
        except:
            raise Exception('Error formatting dataframe')

    return pd.DataFrame(schedules_rows)
