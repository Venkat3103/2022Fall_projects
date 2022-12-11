"""
Hypothesis 4: Toss decision directly contributes to the result of the game.
Author : Burzin Navroze Wadia
Net ID : bwadia2
"""
from typing import Tuple, Any

# Importing Libraries
import pandas as pd
import plotly
import plotly.express as px
import numpy as np
from pandas import DataFrame


def process(unprocessed_df: pd.DataFrame, season: int) -> pd.DataFrame:
    """
    This function takes in Raw DataFrame and year from the user and filters the DataFrame to keep data related to the
    year 2018.

    param unprocessed_df: The Raw DataFrame consisting of data related to Team1 VS Team2, toss_winner, toss_decision, match_winner, year.
    :param season: The season year that the needs to be filtered for.
    :return: Processed or filtered DataFrame wrt year.

    >>> x = pd.read_csv("ipl_match_info.csv", usecols=['Team1', 'Team2', 'date', 'venue', 'toss_winner', 'toss_decision','match_winner', 'year'])
    >>> process(x,2018) # doctest: +ELLIPSIS
                              Team1  ...  year
    0                Mumbai Indians  ...  2018
    1              Delhi Daredevils  ...  2018
    ...

    >>> t_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2019]})
    >>> len(process(t_df, 2018))
    5

    >>> len(process(t_df, 2019))
    1

    >>> t = process(t_df, 2018)
    >>> type(t["year"][0])
    <class 'numpy.int64'>

    """
    if season != "all":
        unprocessed_df = unprocessed_df[unprocessed_df["year"] == season]

    else:
        # Preprocess Data for all the year
        unprocessed_df['Team1'] = unprocessed_df['Team1'].replace(['Delhi Daredevils'], 'Delhi Capitals')
        unprocessed_df['Team2'] = unprocessed_df['Team2'].replace(['Delhi Daredevils'], 'Delhi Capitals')
        unprocessed_df['toss_winner'] = unprocessed_df['toss_winner'].replace(['Delhi Daredevils'], 'Delhi Capitals')
        unprocessed_df['match_winner'] = unprocessed_df['match_winner'].replace(['Delhi Daredevils'], 'Delhi Capitals')

    return unprocessed_df


def overall_plot(processed_df: pd.DataFrame, season: int) -> tuple[None, pd.DataFrame]:
    """
    This function will use the Processed DataFrame from process() and plot data showing the number of matches won by each team based on the individual decision

    param processed_df: Input DataFrame which is the output of process() and also a filtered by year DataFrame

    >>> t_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2018]})
    >>> x,y = overall_plot(t_df, 2018)
    >>> y
              Match Winner toss_decision  Number of Matches Won
    0  Chennai Super Kings         field                      4
    1       Delhi Capitals         field                      1
    2      Kings XI Punjab         field                      1

    >>> y["toss_decision"].unique().tolist()
    ['field']

    """
    # Number of Toss won by each Team during the IPL Season of 2018, 2019, 2020

    match_won = pd.DataFrame(processed_df.groupby(["match_winner", "toss_decision"])["match_winner"].count())
    match_won = match_won.rename(columns={'match_winner': 'Number of Matches Won'})
    match_won.reset_index(inplace=True)
    match_won = match_won.rename(columns={'match_winner': "Match Winner"})
    match_won.head()

    colors = plotly.colors.qualitative.Prism
    fig = px.bar(match_won, x='Match Winner', y='Number of Matches Won', color='toss_decision',
                 text=match_won['Number of Matches Won'].astype(str), color_discrete_sequence=colors)
    fig.update_layout(title_text=f'Toss Decision vs Matches Won for :  {season} Season')

    return fig.show(), match_won


# % of games a team won the toss, won the match
def toss_plot(processed_df: pd.DataFrame, season: int) -> tuple[None, DataFrame]:
    """
    This functions takes the filtered DataFrame as input and plots a piechart of Toss won  vs % matches won and loss.

    param processed_df: Input Filtered DataFrame from process()

    >>> tp_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2018]})
    >>> x,y = toss_plot(tp_df, 2018)
    >>> y
                              Toss_Won  count
    0  Won the Toss and Lost the Match      2
    1   Won the Toss and Won the Match      4

    >>> type(y["count"][0])
    <class 'numpy.int64'>

    >>>

    """

    winner_toss = pd.DataFrame(processed_df[["toss_winner", "match_winner"]])

    winner_toss['Toss_Won'] = np.where((winner_toss['toss_winner'] == winner_toss['match_winner']), "Won the Toss and "
                                                                                                    "Won the Match",
                                       np.where((winner_toss['toss_winner'] != winner_toss['match_winner']),
                                                "Won the Toss and Lost the Match",
                                                np.nan))
    count_df = pd.DataFrame(winner_toss.groupby("Toss_Won")["Toss_Won"].count())
    count_df.rename(columns={"Toss_Won": "count"}, inplace=True)
    count_df.reset_index(inplace=True)

    fig = px.pie(count_df, values="count", names='Toss_Won')

    fig.update_layout(title_text=f'Toss results vs % of Matches Won for :  {season} Season')

    return fig.show(), count_df


def decision_plot(process_data: pd.DataFrame, season: int) -> tuple[None, DataFrame]:
    """
    This functions takes the filtered DataFrame as input and plots a piechart of Winning Toss Decision vs % matches won and loss.

    param process_data: Input Filtered DataFrame from process()

    >>> dp_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2018]})
    >>> x, y = decision_plot(dp_df, 2018)
    >>> y
                                    Bat_Won  count
    0                        Lost the Toss       2
    1  Won the toss and chose to Bat Second      4

    >>> print(type(y))
    <class 'pandas.core.frame.DataFrame'>

    """

    # % of games a team chose batting first, won the match
    winner_bat = pd.DataFrame(process_data[["Team1", "Team2", "toss_winner", "toss_decision", "match_winner"]])

    winner_bat['Bat_Won'] = np.where((winner_bat['toss_winner'] == winner_bat['match_winner']) & (
            winner_bat['toss_decision'] == "bat"), "Won the toss and chose to Bat First",
                                     np.where((winner_bat['toss_winner'] == winner_bat['match_winner']),
                                              "Won the toss and chose to Bat Second", " Lost the Toss "))
    winner_bat.dropna(inplace=True)
    count_df = pd.DataFrame(winner_bat.groupby("Bat_Won")["Bat_Won"].count())

    count_df.rename(columns={"Bat_Won": "count"}, inplace=True)

    count_df.reset_index(inplace=True)

    fig = px.pie(count_df, values="count", names='Bat_Won')

    fig.update_layout(title_text=f'Winning Toss Decision vs % of Matches Won for :  {season} Season')

    return fig.show(), count_df

# --------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    # Defining User Parameters

    # Which IPL season do you want to check the statistics for ?
    season = 2018

    # Reading csv file
    toss_df = pd.read_csv("ipl_match_info.csv",
                          usecols=['Team1', 'Team2', 'date', 'venue', 'toss_winner', 'toss_decision',
                                   'match_winner', 'year'])

    # Variable to store the filtered DataFrame as returned by the process()
    process_df = process(toss_df, season)

    ov_plot, ov_df = overall_plot(toss_df, season)
    print(ov_df)

    t_plot,t_df = toss_plot(process_df, season)
    print(t_df)

    d_plot,d_df = decision_plot(process_df, season)
    print(d_df)


