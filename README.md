# Improving Match xG Infographics

The repository consists of the code used in my blog post about the poisson distribution of Expected Goals in single football matches.

http://roensholt-stats.com/2021-04-25-Hvorfor-expected-goals-ikke-fort%C3%A6ller-resultatet-af-en-kamp/

This project I will make my attempt to improve the common used Expected Goals (xG) race chart from a single game.
This will be done by adding more context like win, loss and draw probabilities, the 3 most probable scorelines and the probability for goals for each team.

- `utils` contains utility functions and scripts for calculations, cleaning and metatdata
- `output` contains all the visualizations
- `team_logos` contains all Premier League team badges
- `xG_Infographic.ipynb` code for the complete xG Infographic
- `goal_probabilities_plot.py` code for goal probability viz
- `win_probability_plot.py` code for win probability viz
- `xG_racechart_plot.py` code for xG racechart viz

## xG Infographic

<img src="output/Leeds_vs_Liverpool_xG_Infographic_gw32.png" width="600" height="400" />

## xG infographic breakdown

**xG racechart**

<img src="output/Leeds_vs_Liverpool_xG_racechart_gw32.png" width="300" height="200" />

**Goal probabilities for each team**

Bar chart of 0-9 goals for each team, where the actual goal(s) scored is filled.

<img src="output/goal_probabilities_viz.png" width="225" height="300" />

**Win probability**

The probability of each team winning or a draw result based on the shots they have taken.

<img src="output/win_probability_viz.png" width="500" height="125" />

