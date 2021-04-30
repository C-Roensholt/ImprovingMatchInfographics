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


# --------------- Create plot ------------------- #
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (6,9))
fig.set_facecolor(facecolor)
ax1.set_facecolor(facecolor)
ax2.set_facecolor(facecolor)


# ------- ax1 -------- #
ax1.bar(home_xs, home_ys,
        facecolor=facecolor, edgecolor=home_color, zorder=10, alpha=1)
for i in home_xs:
    if i == home_goals:
        ax1.bar(i, home_ys[i],
        color=home_color, zorder=10, alpha=1)
#set up our base layer
ax1.tick_params(axis='x', colors='w', labelsize=12)
ax1.set_xticks(home_xs)
ax1.tick_params(axis='y', colors='w', labelsize=12)

# Set grid, ticks and frame
#ax1.grid(axis='y', color='w', linestyle='--', zorder=1, alpha=0.5)
ax1.tick_params(axis='both', which='both', left=False, bottom=False)
ax1.set_frame_on(False)

# Set labels and text
ax1.set_xlabel('Mål',
               color='w', fontweight='bold', size=14)
ax1.set_ylabel('Sandsynlighed',
               color='w', fontweight='bold', size=14)

fig_text(s=f'<{home_team}>', x=0.85, y=0.8,
        highlight_colors=[home_color], highlight_weights=['bold'], fontsize=26, fontweight='bold', ha='right')

# ------- ax2 ---------- #
ax2.bar(away_xs, away_ys,
        facecolor=facecolor, edgecolor=away_color, zorder=10, alpha=1)
for i in away_xs:
    if i == away_goals:
        ax2.bar(i, away_ys[i],
        color=away_color, zorder=10, alpha=1)

#set up our base layer
ax2.tick_params(axis='x', colors='w', labelsize=12)
ax2.set_xticks(away_xs)
ax2.tick_params(axis='y', colors='w', labelsize=12)

# Set grid, ticks and frame
#ax1.grid(axis='y', color='w', linestyle='--', zorder=1, alpha=0.5)
ax2.tick_params(axis='both', which='both', left=False, bottom=False)
ax2.set_frame_on(False)

# Set labels and text
ax2.set_xlabel('Mål',
               color='w', fontweight='bold', size=14)
ax2.set_ylabel('Sandsynlighed',
               color='w', fontweight='bold', size=14)

# Add team names
fig_text(s=f'<{away_team}>', x=0.85, y=0.4,
        highlight_colors=[away_color], highlight_weights=['bold'], fontsize=26, fontweight='bold', ha='right')

#plt.savefig('output/goal_probabilities_viz.png',
#            dpi=600, bbox_inches='tight')


plt.show()