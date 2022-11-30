import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
from matplotlib import ticker
import numpy as np
import plotly.graph_objects as go


def SeasonData(df, season):
    """
    Separates Data into different dataframes as for the required season year

    df: The Team DataFrame which provides information about the players played for a team for each season
    return: It does not return but instead creates variables having dataframes, and stores in the memory. (ex. season_2018)

    >>> SeasonData(pd.DataFrame({"Team":["Chennai Super Kings", "Sunrisers Hyderabad" ] ,
    "date": ["2018-04-07", "2019-05-17"], "player1": ["A","B"] , "player2": ["A","B"] , "player3": ["A","B"] ,
    "player4": ["A","B"] , "player5": ["A","B"] ,"player6": ["A","B"],"player7": ["A","B"] ,
                                 "player8": ["A","B"] ,"player9": ["A","B"] ,"player10": ["A","B"] ,
                                 "player11": ["A","B"] ,"year": [2018,2019]})

    """
    # User input at the very beginning of the file should be the season year

    # preprocessing of the dataframe
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = pd.DatetimeIndex(df['date']).year
    df.drop(columns="Unnamed: 0", inplace=True)

    # Dynamic Variable Name for the dataset related to that specific season year
    for i in team_df["year"].unique():
        globals()[f'season_{i}'] = pd.DataFrame(team_df[team_df["year"] == i].sort_values(by=['Team', 'date']))

    # Returns Dataframe for a season with variable name like "season_2018" if season = 2018
    return globals()[f'season_{season}']


def player_count(season_df):
    """

    :param season_df:
    :return:
    """
    p1 = season_df.groupby(['Team', 'player1'])['player1'].count().to_frame().rename(columns={"player1": "count1"})
    p2 = season_df.groupby(['Team', 'player2'])['player2'].count().to_frame().rename(columns={"player2": "count2"})
    p3 = season_df.groupby(['Team', 'player3'])['player3'].count().to_frame().rename(columns={"player3": "count3"})
    p4 = season_df.groupby(['Team', 'player4'])['player4'].count().to_frame().rename(columns={"player4": "count4"})
    p5 = season_df.groupby(['Team', 'player5'])['player5'].count().to_frame().rename(columns={"player5": "count5"})
    p6 = season_df.groupby(['Team', 'player6'])['player6'].count().to_frame().rename(columns={"player6": "count6"})
    p7 = season_df.groupby(['Team', 'player7'])['player7'].count().to_frame().rename(columns={"player7": "count7"})
    p8 = season_df.groupby(['Team', 'player8'])['player8'].count().to_frame().rename(columns={"player8": "count8"})
    p9 = season_df.groupby(['Team', 'player9'])['player9'].count().to_frame().rename(columns={"player9": "count9"})
    p10 = season_df.groupby(['Team', 'player10'])['player10'].count().to_frame().rename(columns={"player10": "count10"})
    p11 = season_df.groupby(['Team', 'player11'])['player11'].count().to_frame().rename(columns={"player11": "count11"})

    p1.reset_index(inplace=True)
    p2.reset_index(inplace=True)
    p3.reset_index(inplace=True)
    p4.reset_index(inplace=True)
    p5.reset_index(inplace=True)
    p6.reset_index(inplace=True)
    p7.reset_index(inplace=True)
    p8.reset_index(inplace=True)
    p9.reset_index(inplace=True)
    p10.reset_index(inplace=True)
    p11.reset_index(inplace=True)

    p1.rename(columns={"player1": "player", "count1": "count"}, inplace=True)
    p2.rename(columns={"player2": "player", "count2": "count"}, inplace=True)
    p3.rename(columns={"player3": "player", "count3": "count"}, inplace=True)
    p4.rename(columns={"player4": "player", "count4": "count"}, inplace=True)
    p5.rename(columns={"player5": "player", "count5": "count"}, inplace=True)
    p6.rename(columns={"player6": "player", "count6": "count"}, inplace=True)
    p7.rename(columns={"player7": "player", "count7": "count"}, inplace=True)
    p8.rename(columns={"player8": "player", "count8": "count"}, inplace=True)
    p9.rename(columns={"player9": "player", "count9": "count"}, inplace=True)
    p10.rename(columns={"player10": "player", "count10": "count"}, inplace=True)
    p11.rename(columns={"player11": "player", "count11": "count"}, inplace=True)

    count_df = (pd.concat([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]))
    count_df = count_df.groupby(["Team", "player"])[["player", "count"]].sum()
    count_df.reset_index(inplace=True)

    return count_df


def plot_consistency(df_count):
    """

  :param df_count:
  """
    plot_list = df_count["Team"].unique().tolist()

    for i in plot_list:
        plot_df = pd.DataFrame()

        plot_df = df_count[df_count["Team"] == i]

        plot_df["percentage"] = round((plot_df["count"] / len(plot_df["count"])) * 100, 2)

        plot_df.sort_values(by=['percentage'], ascending=False, inplace=True)

        x = plot_df["player"]
        y = plot_df["percentage"]

        # Use textposition='auto' for direct text
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
            marker_color='rgb(55, 83, 109)'
        )])

        fig.update_layout(
            title_text=f'{i} : Players Selection Consistency % for each match',
            uniformtext=dict(mode="hide", minsize=10))

        return fig.show()


if __name__ == "__main__":
    team_df = pd.read_csv("teamsheet.csv")

    season_df = SeasonData(team_df, 2018)

    count_df = player_count(season_df)

    plot_consistency(count_df)
