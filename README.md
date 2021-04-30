# Improving Match xG Infographics

In this project I will make my attempt to improve the common used Expected Goals (xG) race chart from a single game.
This will be done by adding more context like win, loss and draw probabilities, the 3 most probable scorelines and the probability for goals for each team.

- `probability_functions.py` contains functions for calculating win, loss and draw probabilities, scoreline probabilities and probabilities for 0-10 goals for each team
- `xG_Infographic.ipynb` contains loading and preperation of the data, and also the code for the visualizations of the seperate parts and the complete "improved" xG Infographic
- `output` contains all the visualizations

## xG infographic breakdown
- **xG racechart**

<img src="output/Leeds_vs_Liverpool_xG_racechart_gw32.png" width="300" height="200" />

- **Goal probabilities for each team**

Bar chart of 0-9 goals for each team, where the actual goal(s) scored is filled.

<img src="output/goal_probabilities_viz.png" width="225" height="300" />

- **Win probability**

<img src="output/win_probability_viz.png" width="500" height="125" />

