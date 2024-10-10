import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players    
import matplotlib.pyplot as plt
import numpy as np


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
def get_career_stats(player_id):
    career = playercareerstats.PlayerCareerStats(player_id = player_id)
    career_df = career.get_data_frames()[0]
    career_df = career_df[career_df['SEASON_ID'].str[:4].astype(int) <= pd.Timestamp.now().year]

    return career_df

def calculate_average_stats(career_df):
    career_df['PTS/G'] = career_df['PTS'] / career_df['GP']
    career_df['AST/G'] = career_df['AST'] / career_df['GP']
    career_df['REB/G'] = career_df['REB'] / career_df['GP']
    career_df['STL/G'] = career_df['STL'] / career_df['GP']
    career_df['BLK/G'] = career_df['BLK'] / career_df['GP']
    avg_stats = {
        'PTS/G': round(career_df['PTS/G'].mean(),2),
        'AST/G': round(career_df['AST/G'].mean(), 2),
        'REB/G': round(career_df['REB/G'].mean(),2),
        'FT_PCT': round(career_df['FT_PCT'].mean(),2),
        'FG3_PCT': round(career_df['FG3_PCT'].mean(),2),
        'STL/G': round(career_df['STL/G'].mean(),2),
        'BLK/G': round(career_df['BLK/G'].mean(),2)
    }
    return avg_stats

def display_comparison(player1_name, player1_averages, player2_name, player2_averages):
    print(f"\nComparison of {player1_name} vs {player2_name}:")
    print(f"{'Stat':<15}{player1_name:<15}{player2_name:<15}")
    print(f"{'-'*45}")
    print(f"{'Points':<15}{player1_averages['PTS/G']:<15}{player2_averages['PTS/G']:<15}")
    print(f"{'Assists':<15}{player1_averages['AST/G']:<15}{player2_averages['AST/G']:<15}")
    print(f"{'Rebounds':<15}{player1_averages['REB/G']:<15}{player2_averages['REB/G']:<15}")
    print(f"{'FT%':<15}{player1_averages['FT_PCT']:<15}{player2_averages['FT_PCT']:<15}")
    print(f"{'3P%':<15}{player1_averages['FG3_PCT']:<15}{player2_averages['FG3_PCT']:<15}")
    print(f"{'Steals':<15}{player1_averages['STL/G']:<15}{player2_averages['STL/G']:<15}")
    print(f"{'Blocks':<15}{player1_averages['BLK/G']:<15}{player2_averages['BLK/G']:<15}")

def plot_comparison(player1_name, player1_stats, player2_name, player2_stats):
    categories = ['Points', 'Assists', 'Rebounds']
    player1_values = [player1_stats['PTS/G'], player1_stats['AST/G'], player1_stats['REB/G']]
    player2_values = [player2_stats['PTS/G'], player2_stats['AST/G'], player2_stats['REB/G']]
    
    # Define the bar width and the positions of the bars
    bar_width = 0.35
    index = range(len(categories))
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Plot bars for both players
    ax.bar(index, player1_values, bar_width, label=player1_name)
    ax.bar([i + bar_width for i in index], player2_values, bar_width, label=player2_name)
    
    # Add labels and title
    ax.set_xlabel('Stat Category')
    ax.set_ylabel('Values')
    ax.set_title(f'{player1_name} vs {player2_name} - Stats Comparison')
    ax.set_xticks([i + bar_width / 2 for i in index])  # Set the position of the x ticks
    ax.set_xticklabels(categories)  # Set category labels on x-axis
    ax.legend()
    
    # Display the plot
    plt.show()



player1_name = input("Enter the first player's name: ")
player2_name = input("Enter the second player's name: ")

player1_id = get_player_id(player1_name)
player2_id = get_player_id(player2_name)

if player1_id and player2_id:
    player1_stats = get_career_stats(player1_id)
    player2_stats = get_career_stats(player2_id)

    player1_averages = calculate_average_stats(player1_stats)
    player2_averages = calculate_average_stats(player2_stats)

display_comparison(player1_name, player1_averages, player2_name, player2_averages)


plot_comparison(player1_name, player1_averages, player2_name, player2_averages)

