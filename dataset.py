"Author : Amine Rguig"


import csv
from collections import defaultdict
import numpy as np


class FootballDataset:
    """ "
    Football Dataset Class for Datasets from 'football-data.co.uk'

    """

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []  # List of Games

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(row)

    def team_names(self):
        """
        Fetch team names from the dataset.
        """
        team_names = {}
        counter = 1
        unique_team_names = []
        for row in self.data:
            home_team = row["HomeTeam"]
            away_team = row["AwayTeam"]
            if home_team not in unique_team_names:
                unique_team_names.append(home_team)
                team_names[counter] = home_team
                counter += 1
            if away_team not in unique_team_names:
                unique_team_names.append(away_team)
                team_names[counter] = away_team
                counter += 1
        return team_names

    def average_over_under_2_5(self):
        """""
        Average Odds of Over or Under 2.5 Goals

        """ ""

        total_over_2_5 = 0
        total_under_2_5 = 0
        count = 0

        for row in self.data:
            if row["Avg>2.5"] and row["Avg<2.5"]:
                total_over_2_5 += float(row["Avg>2.5"])
                total_under_2_5 += float(row["Avg<2.5"])
                count += 1

        return {
            "average_over_2_5": total_over_2_5 / count,
            "average_under_2_5": total_under_2_5 / count,
        }

    def match_results(self):
        """"
        Result of games

        """ ""
        results = defaultdict(int)
        for row in self.data:
            results[row["FTR"]] += 1
        return dict(results)

    def get_odds(self):
        """
        Getting Odds Implied Probabilities from bookies odds
        """
        Over = []
        Under = []
        for i in range(len(self.data)):
            try:
                over_odds = float(self.data[i]["Max>2.5"])
                under_odds = float(self.data[i]["Max<2.5"])
                Over.append(1 / over_odds)
                Under.append(1 / under_odds)
            except ValueError:

                print(f"Invalid value for odds at index {i}")
                # Calculate mean of valid odds and append
                print(float(self.data[i]["Max>2.5"]),
                      float(self.data[i]["Max<2.5"]))
        return Under, Over

    def get_y(self):
        """""
        Getting Results
        returns list of results : 1 if Over 2.5 Goals, 0 if Under 2.5 Goals



        """ ""
        y = np.zeros(len(self.data))
        for i in range(len(self.data)):
            s = int(self.data[i]["FTHG"]) + int(self.data[i]["FTAG"])
            if s > 2:
                y[i] = 1
        return y

    def construct_features(self, teams, i):
        """""
        Features from  ratings
        """ ""
        Home = self.data[i]["HomeTeam"]
        Away = self.data[i]["AwayTeam"]

        jh = int(
            [k for k in range(1, 21) if self.team_names()[k] == Home][0]) - 1

        ja = int(
            [k for k in range(1, 21) if self.team_names()[k] == Away][0]) - 1

        Homefeature = teams[jh].get_features(True)
        Awayfeature = teams[ja].get_features(False)

        return Homefeature + Awayfeature

    def ranking(self, team_names):
        """
        Team Rankings by points
        """
        Rankings = np.zeros(20)
        for i in range(len(self.data)):
            Home = self.data[i]["HomeTeam"]
            Away = self.data[i]["AwayTeam"]
            jh = int([k for k in range(1, 21) if team_names[k] == Home][0]) - 1
            ja = int([k for k in range(1, 21) if team_names[k] == Away][0]) - 1
            if self.data[i]["FTR"] == "H":
                Rankings[jh] += 3
            elif self.data[i]["FTR"] == "D":
                Rankings[jh] += 1
                Rankings[ja] += 1
            else:
                Rankings[ja] += 3

        sorted_indices = sorted(
            range(len(Rankings)), key=lambda i: Rankings[i], reverse=True
        )
        ranking_dict = {}
        for i in range(20):
            team_name = team_names[sorted_indices[i] + 1]
            points = Rankings[sorted_indices[i]]
            ranking_dict[team_name] = points
        return ranking_dict

    def Releguated(self):

        Rank = self.ranking(self.team_names())
        Releguated = Rank[17:]

        return Releguated
