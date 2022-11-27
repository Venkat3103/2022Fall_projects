import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
from matplotlib import ticker
import numpy as np

toss_df = pd.read_csv("ipl_match_info.csv", usecols=['Team1', 'Team2', 'date', 'venue', 'toss_winner', 'toss_decision'
                      , 'match_winner', 'year'])

toss_df['Team1'] = toss_df['Team1'].replace(['Delhi Daredevils'],'Delhi Capitals')
toss_df['Team2'] = toss_df['Team2'].replace(['Delhi Daredevils'],'Delhi Capitals')
toss_df['toss_winner'] = toss_df['toss_winner'].replace(['Delhi Daredevils'],'Delhi Capitals')
toss_df['match_winner'] = toss_df['match_winner'].replace(['Delhi Daredevils'],'Delhi Capitals')

# Number of Toss won by each Team during the IPL Season of 2018, 2019, 2020

toss_team = pd.DataFrame(toss_df.groupby(["toss_winner","toss_decision"])["toss_winner"].count())
toss_team = toss_team.rename(columns={'toss_winner': 'Number of Tosses Won'})
toss_team.reset_index(inplace = True)
toss_team.head()

fig = px.bar(toss_team, x='toss_winner', y='Number of Tosses Won', color = 'toss_decision',
             text=toss_team['Number of Tosses Won'].astype(str),
             title="Number of Tosses won for each type and each team")

fig.show()

# --------------------------------------------------------------------------------------------------------------------

