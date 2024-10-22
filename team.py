""""Author: Amine Rguig """ ""


class Team:
    """""
    Teams Class for General Attacking Performance Ratings
    
    """ ""

    def __init__(self, num, team_names):
        self.HA = 0  # Home Attacking Rating
        self.HD = 0  # Home Defending Rating
        self.AA = 0  # Away Attacking Rating
        self.AD = 0  # Away Defending Rating
        self.num = num  # Team Number
        self.name = team_names[num]  # Team name
        self.league = "Premier League"  # Team league

    def init(self):
        """""
        Initialize Ratings 
        
        """ ""
        self.HA, self.HD, self.AA, self.AD = 0, 0, 0, 0

    def update(self, HA, HD, AA, AD):
        """""
        Updating Ratings
        
        """ ""
        self.HA = HA
        self.HD = HD
        self.AA = AA
        self.AD = AD

    def get(self):
        """"" 
        Get Ratings 
        """ ""
        return self.HA, self.HD, self.AA, self.AD

    def get_features(self, homeornot):
        """""
        Generates features for Logistic Regression
        
        homeornot: 1 if the Team is playing home, 0 if  not

        """ ""
        if homeornot:
            return self.HA + self.HD
        else:
            return self.AA + self.AD

    def get_features_2(self, homeornot):
        """""
        Generates features for Logistic Regression
        
        homeornot: 1 if the Team is playing home, 0 if  not

        """ ""
        if homeornot:
            return self.HA, self.HD
        else:
            return self.AA, self.AD


def UpdateGamei(params, i, teams, data, mode="G"):
    """"" 
    Updating Ratings of a Team following Game number j 

    Lambda,phi1,phi2: Parametre of ratings
    team_names: Dictionary of Team names
    i: Number of the Game
    teams: list of teams (from Class Teams)
    dataset: list of games 
    mode: mode of the measure of performance used:
    'G' if goals scored by either teams,
    'S+C' for Shots on target and Corners
    'G+S+C': for goals + shots on target+ corners  
    
    """ ""
    lam, phi_1, phi_2 = params
    team_names = data.team_names()
    dataset = data.data
    Home = dataset[i]["HomeTeam"]  # Home Team name
    Away = dataset[i]["AwayTeam"]  # Away Team name

    if mode == "G":

        Sh = int(dataset[i]["FTHG"])  # Goals Scored By The home team
        Sa = int(dataset[i]["FTAG"])  # Goals Scored By The Away team

    elif mode == "S+C":

        Sh = (
            int(dataset[i]["HST"]) + int(dataset[i]["HC"]) / 3
        )  # Corners + Shots Home
        Sa = (
            int(dataset[i]["AST"]) + int(dataset[i]["AC"]) / 3
        )  # Corners + Shots Away

    elif mode == "G+S+C":

        Sh = (
            1.2 * int(dataset[i]["FTHG"])
            + int(dataset[i]["HST"]) / 4
            + int(dataset[i]["HC"]) / 5
        )
        Sa = (
            1.2 * int(dataset[i]["FTAG"])
            + int(dataset[i]["AST"]) / 4
            + int(dataset[i]["AC"]) / 5
        )

    jh = (
        int([k for k in range(1, 21) if team_names[k] == Home][0]) - 1
    )  # index of the home team

    ja = (
        int([k for k in range(1, 21) if team_names[k] == Away][0]) - 1
    )  # index of the away team

    a, b, c, d = teams[jh].get()  # Current Home Ratings
    u, v, x, y = teams[ja].get()  # Current Away Ratings

    # HOME UPDATES  :

    a_new = max(a + lam * phi_1 * (Sh - 0.5 * (a + y)), 0)  # HA

    c_new = max(c + lam * (1 - phi_1) * (Sh - 0.5 * (a + y)), 0)  # AA

    b_new = max(b + lam * phi_1 * (Sa - 0.5 * (x + b)), 0)  # HD

    d_new = max(d + lam * (1 - phi_1) * (Sa - 0.5 * (x + b)), 0)  # AD

    # AWAY UPDATES :

    x_new = max(x + lam * phi_2 * (Sa - 0.5 * (x + b)), 0)  # AA

    u_new = max(u + lam * (1 - phi_2) * (Sa - 0.5 * (x + b)), 0)  # HA

    y_new = max(y + lam * phi_2 * (Sh - 0.5 * (a + y)), 0)  # AD

    v_new = max(v + lam * (1 - phi_2) * (Sh - 0.5 * (a + y)), 0)  # HD

    a, b, c, d = a_new, b_new, c_new, d_new
    u, v, x, y = u_new, v_new, x_new, y_new
    teams[jh].update(a, b, c, d)
    teams[ja].update(u, v, x, y)


class Team_score:
    def __init__(self, team_names, num, atc=0, defs=0):
        self.alpha_vector = [atc]
        self.beta_vector = [defs]

        self.name = team_names[num]
        self.round = 0

    def update(self, alpha_i, beta_i):
        self.alpha_vector.append(alpha_i)
        self.beta_vector.append(beta_i)
        self.round += 1

    def get_last(self):

        return self.alpha_vector[self.round], self.beta_vector[self.round]
