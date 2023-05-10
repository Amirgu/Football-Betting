# Football Betting project for Over/Under 2.5 Goals Market

Implementation of the following paper :A profitable model for predicting the over/under market in football , Edward Wheatcroft

We implemented a model based on Elo Rating of the Football teams (General Attacking Performance), The Ratings may take into different measure of performance which made the model simple and robust

### Datasets : 

We used the datasets from https://www.football-data.co.uk/ on The 2021/2022 and 2022/2023 Premier League Seasons

The Class dataset is implemented in dataset.py 

### GAP Ratings:

The GAP ratings class and updates were implemented in team.py

### Betting :

Two Betting Strategies were implemented the level stakes betting and the Kelly criterion betting.

### Predicting:

We first initialize GAP parameters with (1,0.5,0.5) for making predictions on the 2021/2022 Season,then optimizing the GAP ratings parameters with minimazing the ignorance score(Log Loss) over the past season, and then making predictions for 2022/2023 Season. 

The model yields 7% net return profit on the 2023 season and this without optimizing the parameters, and without using maximum odds.
### Future Extensions:

Using the Bivariate Poisson Process for predicting Game results

Implementing "Forecasting Football Match Results in National League Competitions Using Score-Driven Time Series Models(Koopman)" for more robust predictions

Improving the betting Strategies using risk minimalization
