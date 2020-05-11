def get_pbp(game_id):
    """Returns a dataframe for any all data of a game 
    Args:
        game_id (string) - converted game_id to match id in rs feed
    Returns:
        pandas.Dataframe: the dataframe for the selected game
    """
    url = f"http://www.nfl.com/feeds-rs/playbyplay/{game_id}.json"
    headers={'User-Agent': 'Mozilla/5.0'}
    print(url)
    
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'HttpError with status code: { err.response.status_code}')
        # Return an empty dataframe
        return pd.DataFrame()
    
    return (json_normalize(json.loads(resp.content.decode('utf-8'))))

def get_drives(alt_game_id):
    """Returns a dataframe for any all drives of a game 
    Args:
        alt_game_id (string) - standardized id to be converted to game_id 
        to match id in rs feed
    Returns:
        pandas.Dataframe: the dataframe of drives for the selected game
    """
    #converter to rs game id
    game_id = alt_game_id
    
    df_game = get_pbp(game_id)

    if df_game.empty:return
    
    df_drives = pd.concat([pd.DataFrame(json_normalize(x)) for x in df['drives']],ignore_index=True)
    return df_drives
def _prepare_drives_df(drive_dict):
    """Private method to restructure the response object into the form we need
    Args:
        drive_dict (dict) - json dict of game data
    Returns:
        pandas.Dataframe: standardized mapping of drive columns
    """
