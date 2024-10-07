import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players    
import plotly.graph_objects as go


# Function to get list of player names
def get_all_players():
    player_dicts = players.get_players()
    player_names = [player['full_name'] for player in player_dicts]

    return (player_names)

# Function to get player ID using player name
def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    else:
        raise ValueError(f"No player found with the name {player_name}")

# Function to get career stats and clean the data
def get_clean_career_stats(player_id):
    career = playercareerstats.PlayerCareerStats(player_id = player_id)
    career_df = career.get_data_frames()[0]
    career_df = career_df[career_df['SEASON_ID'].str[:4].astype(int) <= pd.Timestamp.now().year]

    return career_df

curry = get_player_id('Stephen Curry')
print (get_clean_career_stats(curry))
