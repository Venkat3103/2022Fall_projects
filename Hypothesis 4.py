import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
from matplotlib import ticker
import numpy as np

toss_df = pd.read_csv("ipl_match_info.csv", usecols=['Team1', 'Team2', 'date', 'venue', 'toss_winner', 'toss_decision'
    , 'match_winner', 'year'])

toss_df['Team1'] = toss_df['Team1'].replace(['Delhi Daredevils'], 'Delhi Capitals')
toss_df['Team2'] = toss_df['Team2'].replace(['Delhi Daredevils'], 'Delhi Capitals')
toss_df['toss_winner'] = toss_df['toss_winner'].replace(['Delhi Daredevils'], 'Delhi Capitals')
toss_df['match_winner'] = toss_df['match_winner'].replace(['Delhi Daredevils'], 'Delhi Capitals')

# Number of Toss won by each Team during the IPL Season of 2018, 2019, 2020

toss_team = pd.DataFrame(toss_df.groupby(["toss_winner", "toss_decision"])["toss_winner"].count())
toss_team = toss_team.rename(columns={'toss_winner': 'Number of Tosses Won'})
toss_team.reset_index(inplace=True)
toss_team.head()

fig = px.bar(toss_team, x='toss_winner', y='Number of Tosses Won', color='toss_decision',
             text=toss_team['Number of Tosses Won'].astype(str),
             title="Number of Tosses won for each type and each team")

fig.show()

# --------------------------------------------------------------------------------------------------------------------

# How does Toss Decision has any relation with that team winning the match or not

match_won = pd.DataFrame(toss_df.groupby(["match_winner", "toss_decision"])["match_winner"].count())
match_won = match_won.rename(columns={'match_winner': 'Number of Matches Won'})
match_won.reset_index(inplace=True)
match_won = match_won.rename(columns={'match_winner': "Match Winner"})
match_won.head()

colors = plotly.colors.qualitative.Prism
fig = px.bar(match_won, x='Match Winner', y='Number of Matches Won', color='toss_decision',
             text=match_won['Number of Matches Won'].astype(str), color_discrete_sequence=colors)
fig.show()

# --------------------------------------------------------------------------------------------------------------------

# % of games a team chose batting first, won the match

winner_bat = pd.DataFrame(toss_df[["Team1", "Team2", "toss_winner", "toss_decision", "match_winner"]])

winner_bat['Bat_Won'] = np.where((winner_bat['toss_winner'] == winner_bat['match_winner']) & (
        winner_bat['toss_decision'] == "bat"), "Bat First",
                                 np.where((winner_bat['toss_winner'] == winner_bat['match_winner']),
                                          "Bat Second", np.nan))

ax = sns.countplot(x="Bat_Won", data=winner_bat)

# --------------------------------------------------------------------------------------------------------------------

# % of games a team won the toss, won the match

winner_toss = pd.DataFrame(toss_df[["toss_winner","match_winner"]])
winner_toss

winner_toss['Toss_Won'] = np.where((winner_toss['toss_winner'] == winner_toss['match_winner']), "WonT_WonM", np.where((winner_toss['toss_winner'] != winner_toss['match_winner']), "WonT_LostM",np.nan))
winner_toss

ax = sns.countplot(x="Toss_Won", data=winner_toss)

# --------------------------------------------------------------------------------------------------------------------

