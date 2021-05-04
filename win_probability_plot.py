#%%
#import libraries
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from highlight_text import fig_text, ax_text

import utils.probability_functions as pf
from utils.cleaning import create_team_df, align_dfs, chance_quality
from utils.metadata import *

mpl.rcParams['font.family'] = 'Alegreya Sans'

#load data
comp = 'gw32'
df = pd.read_csv(f'../../data/understat/liverpool/{comp}.csv')

# Create a df for each team (will only work as long as both teams took a shot)
df_home, df_away = create_team_df(df)
home_team, away_team = df_home['team'][0], df_away['team'][0]

# Align dataframes
df_home_final, df_home_final1, df_away_final, df_away_final1 = align_dfs(df, df_home, df_away)

# Find total xG
home_min_final = list(df_home_final['minute'].unique())
away_min_final = list(df_away_final['minute'].unique())
home_cum_xG_final = np.array(df_home_final1)
away_cum_xG_final = np.array(df_away_final1)
home_total_xG = '{:.2f}'.format(round(home_cum_xG_final[-1], 2))
away_total_xG = '{:.2f}'.format(round(away_cum_xG_final[-1], 2))

# Get probability of all scorelines from 0-0 to 9-9
home_goal_probs, away_goal_probs, scoreline_probs = pf.score_probability(float(home_total_xG),
                                                                         float(away_total_xG),
                                                                         num_goals=10)

# Prepare data for plotting
#create xs and ys for bar plots 
home_xs, home_ys = zip(*home_goal_probs)
away_xs, away_ys = zip(*away_goal_probs)

#get number of goals for each team
home_goals = len(df_home[df_home['result'] == 'Goal'])
away_goals = len(df_away[df_away['result'] == 'Goal'])
#get team colors
home_color = home_colors[home_team]
away_color = home_colors[away_team]

# Calculate win and draw probabilities
home_prob, away_prob, draw_prob = pf.win_loss_draw_probs(scoreline_probs)

home_prob = int(round(home_prob*100, 0))
draw_prob = int(round(draw_prob*100, 0))
away_prob = int(round(away_prob*100, 0))

#concat to list
home_away_draw_probs = pd.DataFrame({'outcomes': ['home', 'away', 'draw'], 'probs': [home_prob, away_prob, draw_prob]})

# ------------ Create plot -------------- #
fig, ax = plt.subplots(figsize = (6,1))
fig.set_facecolor(facecolor)
ax.set_facecolor(facecolor)

#set up our base layer
ax.tick_params(axis='x', bottom=False, labelsize=12, colors=facecolor)
ax.tick_params(axis='y', left=False, labelsize=12, colors=facecolor)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

# Plot bars
home = ax.barh(0.5, home_away_draw_probs['probs'][0], edgecolor=home_color,
               fill=True, facecolor=home_color,
               linewidth=3, height=0.8)
draw = ax.barh(0.5, home_away_draw_probs['probs'][1],
               left=home_away_draw_probs['probs'][0], edgecolor=text_color,
               facecolor=text_color, fill=True, linewidth=3, height=0.8)
away = ax.barh(0.5, home_away_draw_probs['probs'][2],
               left=home_away_draw_probs['probs'][0]+home_away_draw_probs['probs'][1], edgecolor=away_color,
               facecolor=away_color, fill=True, linewidth=3, height=0.8)

# Set texts
# Home
ax.text(x=home_prob/2, y=0.5, s=f'{home_prob}%',
        color='k', ha='center', size=20, fontweight='bold')
# Draw
ax.text(x=home_prob+draw_prob/2, y=0.5, s=f'{draw_prob}%',
        color='k', ha='center', size=20, fontweight='bold')
# Away
ax.text(x=home_prob+draw_prob+away_prob/2, y=0.5, s=f'{away_prob}%',
        color='k', ha='center', size=20, fontweight='bold')
# Home
ax.text(x=home_prob/2, y=0.99,
        s=f'{home_team}',
        color=home_color, ha='center', size=20, fontweight='bold')

ax.text(x=home_prob+draw_prob+away_prob/2, y=0.99,
        s=f'{away_team}',
        color=away_color, ha='center', size=20, fontweight='bold')

plt.savefig('output/win_probability_viz.png',
            dpi=600, bbox_inches='tight')

plt.show()