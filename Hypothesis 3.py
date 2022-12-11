"""
Hypothesis 3: Consistency in Team selection improves chances of winning the match
Author : Burzin Navroze Wadia
Net ID : bwadia2

"""

# Importing Libraries
from typing import Tuple, Any
import pandas as pd
import plotly.graph_objects as go
from pandas import DataFrame, Series
from plotly.subplots import make_subplots


def SeasonData(df: DataFrame, season: int) -> DataFrame:
    """
    This function takes the main teamsheet.csv file to filter it according to the season year and gives it as output
    dataframe.

    df: The Team DataFrame which provides information about the players played for a team for each season
    :season: Year value that is provided by the user. Data will be filtered according to the year mentioned.
    return: It returns a dataframe with all data with respect to the year mentioned in the function


    >>> d1= SeasonData(pd.DataFrame({"Unnamed: 0": [0,1,2], "Team":["Chennai Super Kings", "Sunrisers Hyderabad", "Rajasthan Royals" ] , "date": ["2018-04-07", "2019-05-17", "2018-04-01" ], "player1": ["A1","B1","C1"] ,"player2": ["A2","B2","C2"] , "player3": ["A3","B3","C3"] , "player4": ["A4","B4","C4"] , "player5": ["A5","B5","C5"] ,"player6": ["A6","B6","C6"],"player7": ["A7","B7","C7"] ,"player8": ["A8","B8","C8"] ,"player9": ["A9","B9","C9"] ,"player10": ["A10","B10","C10"] ,"player11": ["A11","B11","C11"],"year": [2018,2019,2018]}),2018)
    >>> d1["Team"].tolist()
    ['Chennai Super Kings', 'Rajasthan Royals']

    >>> d1["year"].tolist()
    [2018, 2018]

    >>> d2= SeasonData(pd.DataFrame({"Unnamed: 0": [0,1,2], "Team":["Chennai Super Kings", "Sunrisers Hyderabad", "Rajasthan Royals" ] , "date": ["2018-04-07", "2019-05-17", "2018-04-01" ], "player1": ["A1","B1","C1"] ,"player2": ["A2","B2","C2"] , "player3": ["A3","B3","C3"] , "player4": ["A4","B4","C4"] , "player5": ["A5","B5","C5"] ,"player6": ["A6","B6","C6"],"player7": ["A7","B7","C7"] ,"player8": ["A8","B8","C8"] ,"player9": ["A9","B9","C9"] ,"player10": ["A10","B10","C10"] ,"player11": ["A11","B11","C11"],"year": [2018,2019,2018]}),2019)
    >>> d2["Team"].tolist()
    ['Sunrisers Hyderabad']

    >>> d2[["player1","player2","player3"]]
      player1 player2 player3
    1      B1      B2	   B3

    >>> d2= SeasonData(pd.DataFrame({"Unnamed: 0": [0,1,2], "Team":["Chennai Super Kings", "Sunrisers Hyderabad", "Rajasthan Royals" ] , "date": ["2018-04-07", "2019-05-17", "2018-04-01" ], "player1": ["A1","B1","C1"] ,"player2": ["A2","B2","C2"] , "player3": ["A3","B3","C3"] , "player4": ["A4","B4","C4"] , "player5": ["A5","B5","C5"] ,"player6": ["A6","B6","C6"],"player7": ["A7","B7","C7"] ,"player8": ["A8","B8","C8"] ,"player9": ["A9","B9","C9"] ,"player10": ["A10","B10","C10"] ,"player11": ["A11","B11","C11"],"year": [2018,2019,2018]}),2020)
    >>> d2["Team"].tolist()
    []
    """
    # User input at the very beginning of the file should be the season year

    # preprocessing of the dataframe
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = pd.DatetimeIndex(df['date']).year

    if "Unnamed: 0" in df.columns:
        df.drop(columns="Unnamed: 0", inplace=True)

    team_season = pd.DataFrame(df[df["year"] == season].sort_values(by=['Team', 'date']))

    team_season = team_season.astype({"Team": "str", "player1": "str", "player2": "str", "player3": "str",
                                      "player4": "str", "player5": "str", "player6": "str", "player7": "str",
                                      "player8": "str", "player9": "str", "player10": "str", "player11": "str",
                                      "year": "int"})

    # Returns Dataframe for a season with variable name like "season_2018" if season = 2018

    return team_season


def PlayerCount(season_df: DataFrame) -> DataFrame:
    """
    This function takes seasonal team dataframe which consists of all the information of players for a specific
    season year. The function then aggregates and counts the number of time each player appeared for their team
    for that specific season. It then returns a dataframe of this information.

    param season_df: The input would be the name of the dataframe for a specific season.
    :return: will return a dataframe with all the player count for each team for a specific season year.

    >>> f1 = PlayerCount(pd.DataFrame({ "Team":["Chennai Super Kings", "Sunrisers Hyderabad", "Rajasthan Royals", "Chennai Super Kings", "Chennai Super Kings", "Sunrisers Hyderabad" ] , "date": ["2018-04-07", "2019-05-17", "2018-04-01", '2018-04-03', "2018-07-01", "2018-09-12"  ], "player1": ["A1","B1","C1","A1","A1","B1"] ,"player2": ["A2","B2","C2","A2","A3","B1"] , "player3": ["A3","B3","C3","A1","A3","B2"] , "player4": ["A4","B4","C4","A4","A4","B4"] , "player5": ["A5","B5","C5","A5","A5","B4"] ,"player6": ["A6","B6","C6","A6","A7","B6"],"player7": ["A7","B7","C7","A7","A7","B7"] ,"player8": ["A8","B8","C8","A8","A8","B8"] ,"player9": ["A9","B9","C9","A9","A7","B7"] ,"player10": ["A10","B10","C10","A10","A10","B10"] ,"player11": ["A11","B11","C11","A7","A8","B7"],"year": [2018,2019,2018,2018,2018,2018]}))
    >>> f1[f1["count"] >4]
                      Team player  count
    8  Chennai Super Kings     A7      6

    >>> f1["count"].sum()
    66

    >>> f1["Team"].unique().tolist()
    ['Chennai Super Kings', 'Rajasthan Royals', 'Sunrisers Hyderabad']

    >>> f1.dtypes
    Team      object
    player    object
    count      int64
    dtype: object

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


def PlayerConsistency(df_count: DataFrame, team_name: str) -> tuple[None, Any]:
    """
    This Function takes the output DataFrame from function PlayerCount() as an input and calculate the consistency aka
    % of matches played by a player for his team throughout the season. The output is a bar chart of each team showing
    the consistency of each player selected for all the matches that team played.

    param df_count: DataFrame which will provide the team name , each of its player name and how many matches the
            player played imm total for a whole season.

    param team_name: The name of the Team for which the Player Consistency needs to be checked for.

    :return: Bar Chart of individual player consistency of each team and its respective dataframe

    >>> df = pd.DataFrame({"Team":["Chennai Super Kings", "Sunrisers Hyderabad", "Rajasthan Royals", "Chennai Super Kings", "Chennai Super Kings", "Sunrisers Hyderabad" ], "player":["A1","B1","C1","A2","A3","B2"], "count":[1,2,1,3,2,1]})
    >>> PlayerConsistency(df, "Chennai Super Kings")
    (None,                   Team player  count  percentage
    3  Chennai Super Kings     A2      3      100.00
    4  Chennai Super Kings     A3      2       66.67
    0  Chennai Super Kings     A1      1       33.33)


    >>> x, y = PlayerConsistency(df, "Chennai Super Kings")
    >>> len(y)
    3

    >>> type(y)
    <class 'pandas.core.frame.DataFrame'>

    """

    plot_df = df_count[df_count["Team"] == team_name].copy()

    plot_df["percentage"] = round((plot_df.loc[:, "count"] / len(plot_df.loc[:, "count"])) * 100, 2)

    plot_df.sort_values(by=['percentage'], ascending=False, inplace=True)

    x = plot_df["player"]
    y = plot_df["percentage"]

    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
        marker_color='rgb(55, 83, 109)'
    )])

    fig.update_layout(
        title_text=f'{team_name} : Players Selection Consistency % for each match',
        uniformtext=dict(mode="hide", minsize=10),
        xaxis_title="Team Player Name",
        yaxis_title="% of Matches Played")

    return fig.show(), plot_df


def TeamConsistency(player_count_df: pd.DataFrame, consistency_threshold: int) -> tuple[None, DataFrame]:
    """
    This Function takes the output DataFrame from function PlayerCount() as an input and integer from the user
    as defined by consistency_value variable in the if_main condition. This function then calculates Team Consistency
    i.e. % of players that players equal to or above the consistency_threshold defined by the user. The output is a
    Team's player selection Consistency plot and its DataFrame.

    param player_count_df: DataFrame which will provide the team name , each of its player name and how many matches the
                           player played in total for a whole season.
    param consistency_threshold: A integer describing a percentage value by the user.
    :return: Team's player selection Consistency plot and its DataFrame

    """

    cons_dict = dict()

    team_list = player_count_df["Team"].unique().tolist()

    for i in team_list:
        cons_df = player_count_df[player_count_df["Team"] == i].copy()

        cons_df["percentage"] = round((cons_df.loc[:, "count"] / len(cons_df.loc[:, "count"])) * 100, 2)

        cons_df.sort_values(by=['percentage'], ascending=False, inplace=True)

        count = cons_df[cons_df["percentage"] >= consistency_threshold].count().player

        consistency_per = round(((count / cons_df["player"].count()) * 100), 2)

        cons_dict[i] = consistency_per

    team_cons_df = pd.DataFrame(cons_dict.items(), columns=["Team", "Consistency of Players (%)"])

    x = team_cons_df["Team"]
    y = team_cons_df["Consistency of Players (%)"]

    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
        marker_color='rgb(55, 83, 109)',
    )])

    fig.update_layout(
        title_text=f"Team Selection Consistency % for overall season {season_to_check}",
        uniformtext=dict(mode="hide", minsize=10),
        xaxis_title = "Team Name",
        yaxis_title = f"Overall Team's Consistency (Players Consistent >={consistency_value}%)"

    )

    return fig.show(), team_cons_df


# ----------------------------------------------------------------------------------------------------------------------
def TossSeasonData(toss_df: DataFrame, season: int) -> DataFrame:
    """
    This function takes the ipl_match_info.csv file to filter it according to the season year and gives it as output
    dataframe.

    param df: A DataFrame with information on Teams, Fixtures, Date, Toss Decision, Toss Winner and Match Winner.
    param season: Year value that is provided by the user. Data will be filtered according to the year mentioned.
    :return: It returns a dataframe with all data with respect to the year mentioned in the function


    >>> t_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2019]})
    >>> len(TossSeasonData(t_df, 2018))
    5

    >>> len(TossSeasonData(t_df, 2019))
    1

    >>> t = TossSeasonData(t_df, 2018)
    >>> type(t["year"][0])
    <class 'numpy.int64'>

    """
    # User input at the very beginning of the file should be the season year

    # preprocessing of the dataframe
    toss_df['date'] = pd.to_datetime(toss_df['date'])

    match_season = pd.DataFrame(toss_df[toss_df["year"] == season].sort_values(by=['match_winner', 'date']))

    # Returns Dataframe for a season with variable name like "season_2018" if season = 2018

    return match_season


def MatchesWon(toss_season_df: DataFrame) -> DataFrame:
    """
    The Function simply groups by Team and Counts how many matches have each team won for a season.

    param toss_season_df: Takes the filtered dataframe from TossSeasonData(), data for the respective season.
    :return: DataFrame with Team Name and Number of Matches Won by each team for the specified Season.

    >>> t_df = pd.DataFrame({"Team1":["Mumbai Indians","Kolkata Knight Riders", "Kings XI Punjab","Royal Challengers Bangalore", "Royal Challengers Bangalore", "Delhi Capitals"] , "Team2":["Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Chennai Super Kings", "Rajasthan Royals"], "date":["2018-04-07","2018-04-10","2018-04-15", "2018-04-25", "2018-05-05", "2019-05-18"], "venue":["Wankhede Stadium","MA Chidambaram Stadium", "Punjab Cricket Association IS Bindra Stadium","M.Chinnaswamy Stadium","Maharashtra Cricket Association Stadium","Arun Jaitley Stadium"], "toss_winner":["Chennai Super Kings", "Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings","Chennai Super Kings"], "toss_decision":["field","field","field","field","field","field"], "match_winner":["Chennai Super Kings","Chennai Super Kings","Kings XI Punjab","Chennai Super Kings","Chennai Super Kings","Delhi Capitals"], "year":[2018,2018,2018,2018,2018,2018]})
    >>> MatchesWon(t_df)
              match_winner  Number of Matches Won
    0  Chennai Super Kings                      4
    1       Delhi Capitals                      1
    2      Kings XI Punjab                      1

    >>> MatchesWon(t_df)["Number of Matches Won"].sum()
    6

    """
    win_df = pd.DataFrame(toss_season_df.groupby(["match_winner"])["match_winner"].count())

    win_df.rename(columns={"match_winner": "Number of Matches Won"}, inplace=True)

    win_df.reset_index(inplace=True)

    return win_df


# -------------------------------------------------------------------------------------------------
# Players consistent in their team VS Number of matches won by their team

def hypo_plot(MatchWin_df: DataFrame, TeamConsistency_df: DataFrame):
    """
    Creates a Line Plot of Overall Team Selection Consistency vs Number of Matches Won by the team for a season.
    Using this plot one can understand the explanation behind whether it statisfies the Hypothesis 3 or not.

    param MatchWin_df: output DataFrame of TeamConsistency()
    :param TeamConsistency_df: output DataFrame of TeamConsistency().
    :return: a Line Plot of Overall Team Selection Consistency vs Number of Matches Won by the team for a season.

    """
    plot_df = MatchWin_df.merge(TeamConsistency_df, left_on="match_winner", right_on="Team", how="inner")
    plot_df.sort_values(by="Consistency of Players (%)", inplace=True)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=plot_df["Team"], y=plot_df["Consistency of Players (%)"],
                   name="Overall Team Consistency"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=plot_df["match_winner"], y=plot_df["Number of Matches Won"], name="Matches Won"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"Player's selection consistency VS Number of matches won by their team : Season {season_to_check}"
    )

    # Set x-axis title
    # fig.update_xaxes(title_text="Team")
    fig.update_xaxes(
        tickangle=45,
        title_text="Team",
        title_font={"size": 20},
        title_standoff=25)

    # Set y-axes titles
    fig.update_yaxes(title_text="Team Consistency (%)", secondary_y=False)
    fig.update_yaxes(title_text="Number of Matches Won", secondary_y=True)
    # fig.update_layout(xaxis={'categoryorder': 'total descending'})

    # return plot_df["Number of Matches Won"]
    return fig.show()


if __name__ == "__main__":
    # Defining User Parameters

    # Which IPL season do you want to check the statistics for ?
    season_to_check = 2018

    # Define the % of matches a player played for his team for a season to count him towards team consistency?
    consistency_value = 40


    print(f"The below Team Consistency {consistency_value}% vs Team Wins plots are for the year {season_to_check}")

    # ---------------------------------------------------------------------------------------------------------------------
    # Dataframe 1 : Information of matches, teams and players who played for their team  each of the match.
    team_df = pd.read_csv("teamsheet.csv")

    # Variable to store the dataframe after applying the year filter (season to check )
    team_season_data = SeasonData(team_df, season_to_check)

    # Variable to store the number of times a player played for his team for the season specified
    player_count = PlayerCount(team_season_data)
    print('jdbvbaskvb')
    print(player_count)

    # Bar Plot of the % of matches a player played for his team for the season specified
    plot_list = player_count["Team"].unique().tolist()
    for team in plot_list:
        Pconsistency_plot, Pconsistency_df = PlayerConsistency(player_count, team)

    # A Bar Plot of % of Team Consistency, with individual player consistency >= consistency_value of all the players
    # for each team
    consistency_plot, team_consistency = TeamConsistency(player_count, consistency_value)
    # --------------------------------------------------------------------------------------------------------------------

    # Dataframe 2 : Information of matches, toss decision and match winner for specified season
    toss_df = pd.read_csv("ipl_match_info.csv")

    # Variable to filter and store toss_df data for a specific season.
    toss_season_data = TossSeasonData(toss_df, season_to_check)

    # This variable will store a dataframe with team name and its number of wins for that season as two columns.
    win_info = MatchesWon(toss_season_data)

    # -------------------------------------------------------------------------------------------------------------------

    # Line plot of relation between Team consistency vs Number of Matches won by that team throughout the season.
    hypo_plot(win_info, team_consistency)