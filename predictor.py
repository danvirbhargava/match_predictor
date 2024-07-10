import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def convert_to_value(column):
    return column.str.split('/').str[0].astype(float)

def match_outcome_creator(team1_stats, team2_stats):
    team1_score = team1_stats['Goals'] - team2_stats['Goals conceded']
    team2_score = team2_stats['Goals'] - team1_stats['Goals conceded']
    if team1_score > team2_score: # team1 wins
        return 1
    elif team2_score > team1_score: # team2 wins
        return -1
    else:
        return 0

def predict_match_outcome(team1, team2):
    team1_stats = df[df['team'] == team1].iloc[0]
    team2_stats = df[df['team'] == team2].iloc[0]
    match_features = team1_stats.drop(['team']).tolist() + team2_stats.drop(['team']).tolist()
    match_features_df = pd.DataFrame([match_features])
    prediction = model.predict(match_features_df)
    if prediction == 1:
        print(f'The Winner is: {team1}')
    elif prediction == -1:
        print(f'The Winner is: {team2}')
    else:
        print('The Predicted outcome is: Draw')
    
# Data Preparation
df = pd.read_csv('team_stats.csv')
df.replace({'%': ''}, regex=True, inplace=True)
columns_to_convert = ['Passes completed', 'Short passes completed', 'Medium passes completed', 'Long passes completed',
                      'Backward passes completed', 'Passes completed to left', 'Passes completed to right', 
                      'Crosses completed', 'Clearances completed']
for col in columns_to_convert:
    df[col] = convert_to_value(df[col])
numeric_columns = df.columns.drop('team')
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
features = []
labels = []
teams = df['team'].tolist()
for i in range(len(teams)):
    for j in range(len(teams)):
        if i!=j:
            team1_stats = df.iloc[i]
            team2_stats = df.iloc[j]
            match_features = team1_stats.drop(['team']).tolist() + team2_stats.drop(['team']).tolist()
            match_outcome = match_outcome_creator(team1_stats, team2_stats)
            features.append(match_features)
            labels.append(match_outcome)

features_df = pd.DataFrame(features)
labels_df = pd.Series(labels)


X_train, X_test, y_train, y_test = train_test_split(features_df, labels_df, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
team1 = 'England'
team2 = 'Netherlands'
predict_match_outcome(team1, team2)