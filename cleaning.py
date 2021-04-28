import pandas as pd
import numpy as np

#find team names from dataframe (will only work as long as both teams took a shot)
def create_team_df(df):
    home_team = df['team'].iloc[0]
    away_team = df['team'].iloc[-1]

    #create dataframe for each team
    df_home = df[df['team'] == home_team].reset_index(drop=True)
    df_away = df[df['team'] == away_team].reset_index(drop=True)

    #create cumulative xG column
    df_home['cum_xG'] = df_home['xG'].cumsum()
    df_away['cum_xG'] = df_away['xG'].cumsum()
    
    # Calculate chance quality
    df_home['chance_quality'] = df.apply(lambda row: chance_quality(row), axis=1)
    df_away['chance_quality'] = df.apply(lambda row: chance_quality(row), axis=1)
    
    return df_home, df_away

def align_dfs(df, df_home, df_away):
    df_minutes = pd.DataFrame({'minute': range(0, df['minute'].max()+1, 1)})

    # Merge with home and away dfs
    #Home
    df_home_final = df_minutes.merge(df_home,
                                     on='minute', how='left')[['minute', 'cum_xG']]
    df_home_final.fillna(method='ffill', inplace=True)
    df_home_final.fillna(0, inplace=True)
    df_home_final = df_home_final.merge(df_home,
                                        on='minute', how='left')[['minute', 'cum_xG_x', 'result', 'chance_quality']]
    #Away
    df_away_final = df_minutes.merge(df_away,
                                     on='minute', how='left')[['minute', 'cum_xG']]
    df_away_final.fillna(method='ffill', inplace=True)
    df_away_final.fillna(0, inplace=True)
    df_away_final = df_away_final.merge(df_away,
                                        on='minute', how='left')[['minute', 'cum_xG_x', 'result', 'chance_quality']]

    # Group by minutes to make dataframes the same length
    df_home_final1 = df_home_final.groupby(['minute'])[['cum_xG_x']].max().reset_index()
    df_away_final1 = df_away_final.groupby(['minute'])[['cum_xG_x']].max().reset_index()

    df_home_final1 = df_home_final1['cum_xG_x'].fillna(method='ffill')
    df_away_final1 = df_away_final1['cum_xG_x'].fillna(method='ffill')
    
    return df_home_final, df_home_final1, df_away_final, df_away_final1

def chance_quality(row):
    """
    Calculate chance quality
    """
    if row['xG'] < 0.3:
        return 'small_chance'
    if row['xG'] >= 0.3:
        return 'big_chance'
    return 'no_chance'