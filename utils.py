import pandas as pd
import numpy as np
import math


def find_phase(ball):
    """
    Computes which phase a particular ball belongs to
    :param ball: the ball number in the match
    :return: phase as a string

    >>> find_phase(4.2)
    'powerplay'
    >>> find_phase(15.2)
    'middle overs'
    >>> find_phase(18.0)
    'death overs'
    """

    if ball <= 5.6:
        return "powerplay"
    elif ball <= 15.6:
        return "middle overs"
    else:
        return "death overs"


def adjust_ball_number(df):
    """
    Data recorded in the ball number exceeds 0.6 when there are extra deliveries (wides and no balls bowled)
    returns a dataframe with ball number in the range of .1 and .6.
    :param df: dataframe with ball by ball data
    :return: updated dataframe with ball number in the range 0.1 and 0.6

    >>> test_df = pd.DataFrame({'match_id': {0: 1136564, 1: 1136564, 2: 1136564, 3: 1136564, 4: 1136564, 5: 1136564, 6: 1136564, 7: 1136564}, 'innings': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'ball': {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4, 4: 0.5, 5: 0.6, 6: 0.7, 7: 1.1}, 'bowler': {0: 'B Kumar', 1: 'B Kumar', 2: 'B Kumar', 3: 'B Kumar',4: 'B Kumar',5: 'B Kumar', 6: 'B Kumar', 7: 'B Stanlake'}, 'wides': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: 1.0, 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")},'noballs': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")},'wicket_type': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: 'run out',7: float("nan")}, 'legbyes': {0: float("nan"), 1: float("nan"), 2: float("nan"), 3: float("nan"), 4: float("nan"), 5: float("nan"), 6: float("nan"), 7: float("nan")}})
    >>> #Test data frame has values outside of the legal limit for ball number
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


def replace_team_name(df, old_name, new_name):
    """
    
    :param df: 
    :param old_name: old name of the team which has to be replaced
    :param new_name: new name of the team with which old value has to be replaced
    :return: modified data frame with new team names

    >>> test_df = pd.DataFrame({'bowling_team': {0: 'Delhi Daredevils', 1: 'Delhi Daredevils',2: 'Delhi Daredevils',3: 'Delhi Daredevils',4: 'Delhi Daredevils'},'batting_team': {0: 'Kings XI Punjab',1: 'Kings XI Punjab',2: 'Kings XI Punjab',3: 'Kings XI Punjab',4: 'Kings XI Punjab'}})
    >>> replace_team_name(test_df,"Delhi Daredevils","Delhi Capitals")
           bowling_team     batting_team
    0  Delhi Daredevils  Kings XI Punjab
    1  Delhi Daredevils  Kings XI Punjab
    2  Delhi Daredevils  Kings XI Punjab
    3  Delhi Daredevils  Kings XI Punjab
    4  Delhi Daredevils  Kings XI Punjab

    """
    df.replace(old_name, new_name)
    return df


def compute_total_runs(df):
    """

    :param df:
    :return:
    >>> test_df = pd.DataFrame({'ball': {0: 0.1,
    ... 1: 0.2,
    ... 2: 0.3,
    ... 3: 0.4,
    ... 4: 0.4,
    ... 5: 0.5,
    ... 6: 0.6,
    ... 7: 1.1,
    ... 8: 1.2,
    ... 9: 1.3, 10: 1.4, 11: 1.5, 12: 1.6, 13: 2.1, 14: 2.2, 15: 2.3, 16: 2.4, 17: 2.5, 18: 2.6, 19: 3.1},
    ... 'runs_off_bat': {0: 0, 1: 1, 2: 0, 3: 0, 4: 4, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 2, 11: 0, 12: 3, 13: 4, 14: 0, 15: 4, 16: 1, 17: 1, 18: 0, 19: 0},
    ... 'extras': {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}})

    >>> compute_total_runs(test_df)
        ball  runs_off_bat  extras  total_runs_scored
    0    0.1             0       0                  0
    1    0.2             1       0                  0
    2    0.3             0       0                  1
    3    0.4             0       1                  1
    4    0.4             4       0                  2
    5    0.5             0       0                  6
    6    0.6             0       0                  6
    7    1.1             0       0                  6
    8    1.2             0       0                  6
    9    1.3             0       0                  6
    10   1.4             2       0                  6
    11   1.5             0       0                  8
    12   1.6             3       0                  8
    13   2.1             4       0                 11
    14   2.2             0       0                 15
    15   2.3             4       0                 15
    16   2.4             1       0                 19
    17   2.5             1       0                 20
    18   2.6             0       0                 21
    19   3.1             0       0                 21
    """
    df['total_runs_scored'] = 0
    for i in range(1, len(df)):
        if df['ball'][i] != 0.1 or (df['ball'][i] == 0.1 and df['ball'][i - 1] == 0.1):
            df['total_runs_scored'][i] = df['total_runs_scored'][i - 1] + df['runs_off_bat'][i - 1] + df['extras'][
                i - 1]
    return df


def compute_team_score_and_target(df):
    """

    :param df: the data frame with ball by ball information
    :return: two data frames one for each inning with the team scores for both and additionally target for the second innings
    >>> test_df = pd.read_csv("test_file_1.csv")
    >>> test_df.drop(columns=["Unnamed: 0"],inplace=True)
    >>> i1,i2 = compute_team_score_and_target(test_df)
    >>> out1 = pd.read_csv("out_file_1.csv")
    >>> out1.drop(columns=["Unnamed: 0"],inplace=True)
    >>> i1.equals(out1)
    True
    >>> out2 = pd.read_csv("out_file_2.csv")
    >>> out2.drop(columns=["Unnamed: 0"],inplace=True)
    >>> i2.equals(out2)
    True
    """
    df_inn2 = df[df['innings'] == 2]
    df_inn1 = df[df['innings'] == 1]
    df_inn2['team_score'] = df_inn2['total_runs_scored'] + df_inn2['runs_off_bat'] + df_inn2['extras']
    df_inn1['team_score'] = df_inn1['total_runs_scored'] + df_inn1['runs_off_bat'] + df_inn1['extras']
    trs2 = df_inn2.groupby(['match_id'])['team_score'].max().to_frame()
    trs2.rename(columns={'team_score': 'team_total'}, inplace=True)
    df_inn2 = pd.merge(trs2, df_inn2, on=["match_id"], how="inner")
    trs1 = df_inn1.groupby(['match_id'])['team_score'].max().to_frame()
    trs1.rename(columns={'team_score': 'target'}, inplace=True)
    df_inn2 = pd.merge(trs1, df_inn2, on=["match_id"], how="inner")
    df_inn2['target'] += 1
    return df_inn1, df_inn2


def compute_balls_bowled(ball):
    """
    :param ball: the ball number
    :return: the total number of balls bowled till this point in the inning

    >>> compute_balls_bowled(0.1)
    1.0
    >>> compute_balls_bowled(19.6)
    120.0
    >>> compute_balls_bowled(10.0)
    60.0
    """
    return ball * 10 // 10 * 6 + ball * 10 % 10
