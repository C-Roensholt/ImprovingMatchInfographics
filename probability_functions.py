import numpy as np
import pandas as pd


# Function for poisson distribution
def poisson_distribution(k, lambd):
    return (lambd ** k * np.exp(-lambd)) / np.math.factorial(k)


# Calculate probability for goals scored given expected goals
#define maximum number of goals

def score_probability(home_xG, away_xG, num_goals=10):
    
    #loop through number of goals
    home_goals_dist = []
    away_goals_dist = []
    for goals_scored in range(num_goals):
        prob = poisson_distribution(k=goals_scored, lambd=home_xG)
        home_goals_dist.append([goals_scored, prob])

    for goals_scored in range(num_goals):
        prob = poisson_distribution(k=goals_scored, lambd=away_xG)
        away_goals_dist.append([goals_scored, prob])
        
    #concatenate probs
    x, y = zip(home_goals_dist[1], home_goals_dist[1])
    
    # Calculate probability of scores
    score_probs = [[(x[0], y[0]), x[1]*y[1]] for x in home_goals_dist for y in away_goals_dist]
    score_probs.sort(key=lambda x: x[1], reverse=True)
    
    return home_goals_dist, away_goals_dist, score_probs


# Calculate scoreline probabilities
def win_loss_draw_probs(score_probs):
    draw_prob_list = []
    home_win_prob_list = []
    away_win_prob_list = []
    #loop through scoreline and append home, away or draw scorelines
    #i.e. (1-0, 1-1, 0-1)
    for score, prob in score_probs:
        if score[0] > score[1]:
            home_win_prob_list.append(prob)
        if score[0] < score[1]:
            away_win_prob_list.append(prob)
        if score[0] == score[1]:
            draw_prob_list.append(prob)
    home_win_prob = sum(home_win_prob_list)
    away_win_prob = sum(away_win_prob_list)
    draw_prob = sum(draw_prob_list)
    
    return home_win_prob, away_win_prob, draw_prob

#if __name__=="__main__":
#    main()
    