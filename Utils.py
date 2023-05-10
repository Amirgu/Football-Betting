
"Author : Amine Rguig"


import numpy as np
from team import *
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from Betting import*

def print_team_stats(teams_list):
    # Sort the teams by HA in descending order and get the top one
    ha_max = max(teams_list, key=lambda team: team.HA)
    print(f"The best Home attacking team is: {ha_max.name} ({ha_max.HA})")
    
    # Sort the teams by HD in ascending order and get the top one
    hd_max = min(teams_list, key=lambda team: team.HD)
    print(f"The best Home defensing team is: {hd_max.name} ({hd_max.HD})")
    
    # Sort the teams by AA in descending order and get the top one
    aa_max = max(teams_list, key=lambda team: team.AA)
    print(f"The best Away attacking team is: {aa_max.name} ({aa_max.AA})")
    
    # Sort the teams by AD in ascending order and get the top one
    ad_max = min(teams_list, key=lambda team: team.AD)
    print(f"The best Away defensing team: {ad_max.name} ({ad_max.AD})")
    print('\n')
    # Calculate average attributes
    for team in teams_list:
        team.avg_attr_att = ((team.HA + team.AA) )
    
    # Sort the teams by the average attribute in descending order and get the top one
    top_teams = sorted(teams_list, key=lambda team: team.avg_attr_att, reverse=True)[:5]
    print("The three best overall teams with the highest average attacking attribute are:")
    for team in top_teams:
        print(f"{team.name} ({team.avg_attr_att})")
    print('\n')

    for team in teams_list:
        team.avg_attr_def = ((team.AD + team.HD) )
    
    # Sort the teams by the average attribute in descending order and get the top one
    top_teams = sorted(teams_list, key=lambda team: team.avg_attr_def)[:5]
    print("The three best overall teams with the highest average defending attribute are:")
    for team in top_teams:
        print(f"{team.name} ({team.avg_attr_def})")
    print('\n')

def initialize_burn_in(lam,phi1,phi2,teams,team_names,dataset,burn_in,mode,init_option=True):
    """
    Initializing Ratings for the first matches 

    lam,phi1,phi2: Rating Paramaters
    teams: list of Class Teams
    team_names: Dictionary of team names
    dataset: list of matches
    burn_in: Last match of initialization
    mode: 'G' for goals,'G+S+C' for goals+shots on target + corners

    """
    if init_option:
        for i in range(len(teams)):
            teams[i].init()

    for i in range(burn_in):
        UpdateGamei(lam,phi1,phi2,team_names,i,teams,dataset,mode)

def features_up_tomatchej(lam,phi1,phi2,j,Over,teams,team_names,data,Dataset,mode):
    
    """"
    Construct features from the burn_in matchs (60 matches or more ) to the j matches
    

    lam,phi1,phi2: Rating Paramaters
    teams: list of Class Teams
    team_names: Dictionary of team names
    dataset: list of matches
    Dataset: From Class Dataset
    burn_in: Last match of initialization
    mode: 'G' for goals,'G+S+C' for goals+shots on target + corners
    
    """

    burn_in=62
    X=np.zeros((j-burn_in,3))       #### 3 featurees 1 ,HA+HD+AA+AD, Odds_implied probability of over 2.5
    X[:,0]=np.ones(j-burn_in)
    for k in range(burn_in,j):
        i=k-62
        
        X[i][1]=Dataset.construct_features(team_names,teams,k)

        
        X[i][2]=Over[k]
   

        UpdateGamei(lam,phi1,phi2,team_names,k,teams,data,mode)

    return X    
