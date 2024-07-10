Match Predictor for the 2024 Euros

scra.py uses selenium to gather the teams tournament statistics from the uefa website
and produces a csv file of the statistics
predictor.py uses the csv produced from scra.py and uses the RandomForestClassifier 
from the scikit-learn library to estimate the winner of a match between two given teams
participating the tournament


