# Author: Arjun Kumaran
# Helper Functions for Hypothesis - 2

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import warnings
from matplotlib import rcParams

rcParams['figure.figsize'] = 11.7, 15
warnings.filterwarnings("ignore")


def adjust_ball_number(df):
    """
  returns a dataframe with ball number in the range of .1 and .6
  :param df: dataframe with ball by ball data
  :return df: updated dataframe
   >>> test_df = pd.DataFrame({'match_id': {0: 1136564, 1: 1136564, 2: 1136564, 3: 1136564, 4: 1136564, 5: 1136564, 6: 1136564, 7: 1136564}, 'innings': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'ball': {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4, 4: 0.5, 5: 0.6, 6: 0.7, 7: 1.1}, 'bowler': {0: 'B Kumar', 1: 'B Kumar', 2: 'B Kumar', 3: 'B Kumar',4: 'B Kumar',5: 'B Kumar', 6: 'B Kumar', 7: 'B Stanlake'}, 'wides': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: 1.0, 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")},'noballs': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")},'wicket_type': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: 'run out',7: float("nan")}, 'legbyes': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")}})
   >>> l = [x*10%10 for x in list(test_df.ball.unique())]
   >>> all(x <= 6 for x in l)
   False
   >>> out_df = adjust_ball_number(test_df)
   >>> l = [x*10%10 for x in list(out_df.ball.unique())]
   >>> #Check if all ball numbers are less than or equal to 6 (which is the maximum number of legal deliveries allowed)
   >>> all(x <= 6 for x in l)
   True
  """
    for i in range(1, len(df)):
        if df['match_id'][i] == df['match_id'][i - 1] and df['innings'][i] == df['innings'][i - 1]:
            if (not (math.isnan(df['wides'][i - 1]))) or (
                    not math.isnan(df['noballs'][i - 1])):
                df['ball'][i] = df['ball'][i - 1]
            elif math.floor(df['ball'][i]) == math.floor(df['ball'][i - 1]):
                df['ball'][i] = round(df['ball'][i - 1] + .1, 1)
                if round(df['ball'][i] - math.floor(df['ball'][i]), 1) > 0.6:
                    curi = i
                    while df['ball'][curi] > math.floor(df['ball'][i]) and not df['legbyes'][curi] > 0:
                        df['ball'][curi] = round(df['ball'][curi] - .1, 1)
                        curi -= 1
    return df


def get_batting_data(df: pd.DataFrame):
    """
        Returns a dataframe with batting statistics for each player using the ball by ball dataframe

        :param df: dataframe with ball by ball data :return: batting_data: dataframe with stats for each batsman such as
        batting average, strike rate, total balls faced and so on.
        >>> test_df = pd.read_csv("test_file_2.csv")
        >>> out_df = get_batting_data(test_df)
        >>> out_df[['Batting Average','Batting Strike Rate']].head()
           Batting Average  Batting Strike Rate
        0        11.000000            84.615385
        1         7.000000           116.666667
        2        47.655172           162.206573
        3        24.666667           125.423729
        4        11.666667           100.000000
    """

    no_wides = df[df['wides'].isnull()]
    runs_scored = df.groupby('striker')['runs_off_bat'].sum().to_frame()
    balls_faced = no_wides.groupby('striker')['ball'].count().to_frame()
    outs = df['player_dismissed'].value_counts().rename_axis('striker').to_frame('outs')
    innings_played = df.groupby('striker').match_id.nunique()
    runs_scored.reset_index(inplace=True)
    balls_faced.reset_index(inplace=True)
    outs.reset_index(inplace=True)
    outs = outs.rename(columns={'index': 'striker'})
    outs = outs[outs.striker != "-1"]
    batting_data = pd.merge(
        pd.merge(pd.merge(runs_scored, balls_faced, how="inner", on='striker'), outs, how="inner", on='striker'),
        innings_played, how="inner", on='striker')
    batting_data['Batting Average'] = batting_data['runs_off_bat'] / batting_data['outs']
    batting_data['Batting Strike Rate'] = batting_data['runs_off_bat'] * 100 / batting_data['ball']
    batting_data.rename(columns={'striker': 'Player', 'runs_off_bat': 'Runs Scored', 'ball': 'Balls Faced',
                                 'outs': 'Times Dismissed', 'match_id': 'Innings Played'}, inplace=True)
    return batting_data
