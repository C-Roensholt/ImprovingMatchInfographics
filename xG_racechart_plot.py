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


# ---------- Create plot ---------- #
fig, ax = plt.subplots(figsize = (14,8))
fig.set_facecolor(facecolor)
ax.set_facecolor(facecolor)

ax.set_facecolor(facecolor)
#set up our base layer
ax.tick_params(axis='x', bottom=False, labelsize=12, colors='w')
ax.tick_params(axis='y', left=False, labelsize=12, colors='w')

ax.set_frame_on(False)

#set grid
ax.grid(ls=(0, (5, 10)), lw=.5, color='#c7d5cc', axis='both', zorder=1)
spines = ['top','bottom','left','right']
for x in spines:
    if x in spines:
        ax.spines[x].set_visible(False)
ax.set_xticks([0,15,30,45,60,75,90, 105])


#plot the step graphs
ax.plot(home_min_final, home_cum_xG_final, drawstyle='steps-post',
        color=home_color, label=f'{home_team}', linewidth=5)

ax.plot(away_min_final, away_cum_xG_final, drawstyle='steps-post',
        color=away_color, label=f'{away_team}', linewidth=5)

#plot home goals
for i in range(len(df_home_final)):
    if df_home_final['result'][i] == 'Goal':
        ax.scatter(df_home_final['minute'][i], df_home_final['cum_xG_x'][i], 
                    s=300, zorder=10, facecolor=home_color, label='Mål')
        ax.scatter(df_home_final['minute'][i], df_home_final['cum_xG_x'][i], 
            s=650, zorder=9, facecolor=home_color, alpha=0.3)
for i in range(len(df_away_final)):
    if df_away_final['result'][i] == 'OwnGoal':
        ax.scatter(df_away_final['minute'][i], df_home_final['cum_xG_x'][i], 
                    s=300, zorder=10, facecolor=home_color, label='Mål')
        ax.scatter(df_away_final['minute'][i], df_home_final['cum_xG_x'][i], 
                    s=650, zorder=9, facecolor=home_color, alpha=0.3)
        
#plot away goals
for i in range(len(df_away_final)):
    if df_away_final['result'][i] == 'Goal':
        ax.scatter(df_away_final['minute'][i], df_away_final['cum_xG_x'][i], 
                    s=300, zorder=10, facecolor=away_color, label='Mål')
        ax.scatter(df_away_final['minute'][i], df_away_final['cum_xG_x'][i], 
                    s=650, zorder=9, facecolor=away_color, alpha=0.3)
for i in range(len(df_home_final)):
    if df_home_final['result'][i] == 'OwnGoal':
        ax.scatter(df_home_final['minute'][i], df_away_final['cum_xG_x'][i], 
                    s=300, zorder=10, facecolor=away_color, label='Mål')
        ax.scatter(df_home_final['minute'][i], df_away_final['cum_xG_x'][i], 
                    s=650, zorder=9, facecolor=away_color, alpha=0.3)
        
# Set x and y labels
ax.set_xlabel('Minutter', color='white', fontsize=16)
ax.set_ylabel('Expected Goals (xG)', color='white', fontsize=16)

# Add signature and data source
ax.text(90, -0.3, s='Data | understat.com', ha='right',
        fontsize=10, fontstyle='normal', color='white')
ax.text(90, -0.37, s='twitter.com/C_Roensholt', fontsize=10, fontstyle='normal', color='white', ha='right')

# Add home and away team names
fig_text(x=0.42, y=0.96, s = f'<{home_team}>', 
         fontsize=42, color='white', ha='right', highlight_colors=[home_color],
         highlight_weights='bold')
fig_text(x=0.58, y=0.96, s = f'<{away_team}>', 
         fontsize=42, color='white', ha='left', highlight_colors=[away_color],
         highlight_weights='bold')

# Add home and away goals
fig_text(x=0.5, y=0.96, s = f'<{home_goals}>   -   <{away_goals}>', 
         fontsize=48, color='white', ha='center', highlight_colors=['w', 'w'],
         highlight_weights='bold', fontweight='bold')

# Add home and away xG totals
fig_text(x=0.5, y=0.90, s = f'<{home_total_xG}>   xG   <{away_total_xG}>', 
         fontsize=36, color='white', ha='center', highlight_colors=['w', 'w'],
         highlight_weights='bold', fontweight='bold')


#plt.savefig(f'output/{home_team}_vs_{away_team}_xG_racechart_{comp}.png', dpi=600, 
#            bbox_inches='tight', facecolor=facecolor, edgecolor='none')

plt.show()