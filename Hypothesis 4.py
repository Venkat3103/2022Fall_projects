import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
from matplotlib import ticker
import numpy as np


def process(unprocessed_df, season):
    """

    :param unprocessed_df:
    :return:
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


def overall_plot(processed_df):
    """

    :param processed_df:
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
    fig.show()


# % of games a team won the toss, won the match
def toss_plot(processed_df):
    """

    :param processed_df:
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

    fig.show()


def decision_plot(process_data):
    """

    :param process_data:
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

    fig.update_layout(title_text=f'Toss results vs % of Matches Won for :  {season} Season')

    fig.show()


# --------------------------------------------------------------------------------------------------------------------

# # How does Toss Decision has any relation with that team winning the match or not
#
# match_won = pd.DataFrame(toss_df.groupby(["match_winner", "toss_decision"])["match_winner"].count())
# match_won = match_won.rename(columns={'match_winner': 'Number of Matches Won'})
# match_won.reset_index(inplace=True)
# match_won = match_won.rename(columns={'match_winner': "Match Winner"})
# match_won.head()
#
# colors = plotly.colors.qualitative.Prism
# fig = px.bar(match_won, x='Match Winner', y='Number of Matches Won', color='toss_decision',
#              text=match_won['Number of Matches Won'].astype(str), color_discrete_sequence=colors)
# fig.show()
#
# # --------------------------------------------------------------------------------------------------------------------
#
# # % of games a team chose batting first, won the match
#
# winner_bat = pd.DataFrame(toss_df[["Team1", "Team2", "toss_winner", "toss_decision", "match_winner"]])
#
# winner_bat['Bat_Won'] = np.where((winner_bat['toss_winner'] == winner_bat['match_winner']) & (
#         winner_bat['toss_decision'] == "bat"), "Bat First",
#                                  np.where((winner_bat['toss_winner'] == winner_bat['match_winner']),
#                                           "Bat Second", np.nan))
#
# ax = sns.countplot(x="Bat_Won", data=winner_bat)
#
# # --------------------------------------------------------------------------------------------------------------------
#
# # % of games a team won the toss, won the match
#
# winner_toss = pd.DataFrame(toss_df[["toss_winner", "match_winner"]])
# winner_toss
#
# winner_toss['Toss_Won'] = np.where((winner_toss['toss_winner'] == winner_toss['match_winner']), "WonT_WonM",
#                                    np.where((winner_toss['toss_winner'] != winner_toss['match_winner']), "WonT_LostM",
#                                             np.nan))
# winner_toss
#
# ax = sns.countplot(x="Toss_Won", data=winner_toss)

# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    season = 2018

    toss_df = pd.read_csv("ipl_match_info.csv",
                          usecols=['Team1', 'Team2', 'date', 'venue', 'toss_winner', 'toss_decision',
                                   'match_winner', 'year'])
    process_df = process(toss_df, season)

    overall_plot(process_df)

    toss_plot(process_df)

    decision_plot(process_df)
