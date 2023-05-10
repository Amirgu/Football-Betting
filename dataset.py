
"Author : Amine Rguig"


import csv
from collections import defaultdict
import numpy as np


class FootballDataset:
    """"
    Football Dataset Class for Datasets from 'football-data.co.uk'

    """
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []              #### List of Games 

        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(row)

    def team_names(self):
        """""
        Fetching for team names in the dataset

        """""
        team_names = {}
        counter = 1
        unique_team_names = set()
        for row in self.data:
            unique_team_names.add(row['HomeTeam'])
            unique_team_names.add(row['AwayTeam'])
        for team in unique_team_names:
            team_names[counter] = team
            counter += 1
        return team_names

    def average_over_under_2_5(self):
        """""
        Average Odds of Over or Under 2.5 Goals
        
        """""

        total_over_2_5 = 0
        total_under_2_5 = 0
        count = 0

        for row in self.data:
            if row['BbAv>2.5'] and row['BbAv<2.5']:
                total_over_2_5 += float(row['BbAv>2.5'])
                total_under_2_5 += float(row['BbAv<2.5'])
                count += 1

        return {
            'average_over_2_5': total_over_2_5 / count,
            'average_under_2_5': total_under_2_5 / count
        }

    def match_results(self):
        """"
        Result of games

        """""
        results = defaultdict(int)
        for row in self.data:
            results[row['FTR']] += 1
        return dict(results)


    def get_odds(self):
        """
        Gettings Odds Implied Probabilities from bookies odds 
        """
        Over=[1/float(self.data[i]['Avg>2.5']) for i in range(len(self.data))]
        Under=[1/float(self.data[i]['Avg<2.5']) for i in range(len(self.data))]
        return Under,Over
    
    def get_y(self):
        """""
        Getting Results 

        returns list of results : 1 if Over 2.5 Goals, 0 if Under 2.5 Goals
                                

        
        """""
        y=np.zeros(len(self.data))
        for i in range(len(self.data)):
            s=int(self.data[i]['FTHG'])+int(self.data[i]['FTAG'])
            if s > 2 : 
                y[i]=1
        return y
    

    def construct_features(self,team_names,teams,i):
        """""
        Features from  ratings
        """""
        Home=self.data[i]['HomeTeam']
        Away=self.data[i]['AwayTeam']
       
        

        jh=int([k for k in range(1,21) if team_names[k]== Home ][0]) -1
        
        ja=int([k for k in range(1,21) if team_names[k]== Away ][0])-1

        Homefeature=teams[jh].get_features(True)
        Awayfeature=teams[ja].get_features(False)

        return Homefeature+Awayfeature
    def ranking(self,team_names):

        """""
        Team Rankings by points
        """""
        Rankings=np.zeros(20)
        for i in range(len(self.data)):

            Home=self.data[i]['HomeTeam']
            Away=self.data[i]['AwayTeam']
            jh=int([k for k in range(1,21) if team_names[k]== Home ][0])-1
            ja=int([k for k in range(1,21) if team_names[k]== Away ][0])-1
            if self.data[i]['FTR'] == 'H':
                Rankings[jh]+=3
            elif self.data[i]['FTR'] == 'D':
                Rankings[jh]+=1
                Rankings[ja]+=1
            else:
                Rankings[ja]+=3
        
        sorted_indices = sorted(range(len(Rankings)), key=lambda i: Rankings[i], reverse=True)
        Rank=[]
        for i in range(20):
            Rank.append([ team_names[sorted_indices[i] + 1], Rankings[sorted_indices[i] ] ])
        return Rank
    def Releguated(self,team_names):

        Rank=self.ranking(team_names)
        Releguated=Rank[17:]

        return Releguated

        
    