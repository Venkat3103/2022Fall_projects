import pandas as pd
import numpy as np
import math


def find_phase(ball: float):
    """
    This function tags the phase for each of the balls.
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


def adjust_ball_number(df: pd.DataFrame):
    """
    Data recorded in the ball number exceeds 0.6 when there are extra deliveries (wides and no balls bowled)
    This function returns a dataframe with ball number in the range of .1 and .6.
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
    This function replaces all occurence of an old team name with the new team name.
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


def compute_total_runs(df: pd.DataFrame):
    """
    This function returns a data frame after computing the total runs scored after each ball
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


def compute_team_score_and_target(df: pd.DataFrame):
    """
    This function returns a data frame with the team score and the target.
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


def compute_run_rate(df: pd.DataFrame):
    """
    This function computes the run rate for each of the phases based on the runs scored and the balls bowled in that phase.
    :param df: dataframe updated with run rate

    >>> test_df = pd.DataFrame({'match_id': {0: 1136561, 1: 1136561, 2: 1136561},
    ... 'phase': {0: 'death overs', 1: 'middle overs', 2: 'powerplay'},
    ... 'batting_team': {0: 'Mumbai Indians',
    ...  1: 'Mumbai Indians',
    ... 2: 'Mumbai Indians'},
    ... 'bowling_team': {0: 'Chennai Super Kings',
    ... 1: 'Chennai Super Kings',
    ... 2: 'Chennai Super Kings'},
    ... 'ball': {0: 19.6, 1: 15.6, 2: 5.6},
    ... 'team_score': {0: 165, 1: 121, 2: 39},
    ... 'wickets': {0: 0, 1: 2, 2: 2},
    ... 'balls_bowled': {0: 120.0, 1: 96.0, 2: 36.0},
    ... 'run_rate': {0: 8.25, 1: 7.5625, 2: 6.5}})
    >>> expected_out_df = pd.DataFrame({'match_id': {0: 1136561, 1: 1136561, 2: 1136561},
    ... 'phase': {0: 'death overs', 1: 'middle overs', 2: 'powerplay'},
    ... 'batting_team': {0: 'Mumbai Indians',
    ... 1: 'Mumbai Indians',
    ... 2: 'Mumbai Indians'},
    ... 'bowling_team': {0: 'Chennai Super Kings',
    ... 1: 'Chennai Super Kings',
    ... 2: 'Chennai Super Kings'},
    ... 'ball': {0: 19.6, 1: 15.6, 2: 5.6},
    ... 'team_score': {0: 165, 1: 121, 2: 39},
    ... 'wickets': {0: 0, 1: 2, 2: 2},
    ... 'balls_bowled': {0: 120.0, 1: 96.0, 2: 36.0},
    ... 'run_rate': {0: 11.0, 1: 8.2, 2: 6.5},
    ... 'phase_runs': {0: 44, 1: 82, 2: 39},
    ... 'phase_balls': {0: 24, 1: 60, 2: 36}})
    >>> expected_out_df.equals(compute_run_rate(test_df))
    True
    """
    df['phase_runs'] = 0
    df['run_rate'] = 0.0
    df['phase_balls'] = 0
    for i in range(0, len(df)):
        # print(i)
        if i != len(df) - 1 and df['match_id'][i] == df['match_id'][i + 1]:
            df['phase_balls'][i] = df['balls_bowled'][i] - df['balls_bowled'][i + 1]
            df["phase_runs"][i] = df['team_score'][i] - df['team_score'][i + 1]
            df['run_rate'][i] = df["phase_runs"][i] * 6 / df['phase_balls'][i]
        else:
            df["phase_runs"][i] = df['team_score'][i]
            df['phase_balls'][i] = df['balls_bowled'][i]
            df['run_rate'][i] = df['team_score'][i] * 6 / df['phase_balls'][i]
    df["phase_runs"][i] = df['team_score'][i]
    df['phase_balls'][i] = df['balls_bowled'][i]
    df['run_rate'][i] = df['team_score'][i] * 6 / df['phase_balls'][i]
    # print(i)
    return df


def compute_balls_bowled(ball: float):
    """
    This function computes the number of balls bowled after every single ball.
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


def compute_batting_position(df: pd.DataFrame, match_id: int):
    """
    This function computes the batting position of every batter in each of the games.
    :param df: ball by ball data
    :param match_id: match for which batting positions have to be computed
    :return: data frame with batting positions of each player in a particular match in each of the innings

    >>> pos_df = pd.DataFrame(columns = ["batting_position","match_id","innings","striker"])
    >>> test_df = pd.read_csv("test_file_1.csv")
    >>> test_df.drop(columns=["Unnamed: 0"],inplace=True)
    >>> expected_out_df = pd.DataFrame({'batting_position': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11}, 'match_id': {0: 1136564,  1: 1136564, 2: 1136564, 3: 1136564, 4: 1136564, 5: 1136564, 6: 1136564, 7: 1136564, 8: 1136564, 9: 1136564, 10: 1136564},'innings': {0: 2, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}, 'striker': {0: 'WP Saha', 1: 'S Dhawan', 2: 'KS Williamson', 3: 'BA Stokes', 4: 'RA Tripathi', 5: 'JC Buttler', 6: 'K Gowtham', 7: 'S Gopal', 8: 'DS Kulkarni', 9: 'JD Unadkat', 10: 'B Laughlin'}})
    >>> pos_df = pd.concat([pos_df,compute_batting_position(test_df,1136564)])
    >>> pos_df[['batting_position','innings','striker']]
       batting_position innings        striker
    0                 1       1      AM Rahane
    1                 2       1      DJM Short
    2                 3       1      SV Samson
    3                 4       1      BA Stokes
    4                 5       1    RA Tripathi
    5                 6       1     JC Buttler
    6                 7       1      K Gowtham
    7                 8       1        S Gopal
    8                 9       1    DS Kulkarni
    9                10       1     JD Unadkat
    10               11       1     B Laughlin
    0                 1       2        WP Saha
    1                 2       2       S Dhawan
    2                 3       2  KS Williamson
    """
    df1 = df[(df['match_id'] == match_id) & (df['innings'] == 1)]
    df2 = df[(df['match_id'] == match_id) & (df['innings'] == 2)]
    player_list_1 = pd.unique(df1[['striker', 'non_striker']].values.ravel())
    player_list_2 = pd.unique(df2[['striker', 'non_striker']].values.ravel())
    names1 = list(player_list_1)
    names2 = list(player_list_2)
    match_id_list_1 = [match_id] * len(names1)
    match_id_list_2 = [match_id] * len(names2)
    inn1_list = [1] * len(names1)
    inn2_list = [2] * len(names2)
    zipped1 = list(zip(match_id_list_1, inn1_list, names1))
    zipped2 = list(zip(match_id_list_2, inn2_list, names2))
    inn1_df = pd.DataFrame(zipped1, columns=['match_id', 'innings', 'striker'])
    inn2_df = pd.DataFrame(zipped2, columns=['match_id', 'innings', 'striker'])
    inn1_df.reset_index(inplace=True)
    inn1_df.rename(columns={"index": "batting_position"}, inplace=True)
    inn1_df['batting_position'] = inn1_df['batting_position'] + 1
    inn2_df.reset_index(inplace=True)
    inn2_df.rename(columns={"index": "batting_position"}, inplace=True)
    inn2_df['batting_position'] = inn2_df['batting_position'] + 1
    return pd.concat([inn1_df, inn2_df])


def get_batting_data(df: pd.DataFrame):
    """
    This function summarises the batting statistics for each batting position using the ball by ball data
    :param df: ball by ball data
    :return: summarised batting statistics based on batting position

    >>> test_df = pd.read_csv("test_file_2.csv")
    >>> out_df = get_batting_data(test_df)
    >>> out_df[['Batting Average','Batting Strike Rate']]
        Batting Average  Batting Strike Rate
    0         33.286567           134.365586
    1         32.167665           139.786625
    2         31.715655           132.660698
    3         29.663194           133.944810
    4         23.714844           130.784145
    5         24.535714           144.849398
    6         20.422535           139.155470
    7         12.285714           124.123711
    8          7.774194            90.943396
    9          8.741935            89.438944
    10         4.812500            71.296296
    """
    no_wides = df[df['wides'].isnull()]
    runs_scored = df.groupby('batting_position')['runs_off_bat'].sum().to_frame()
    balls_faced = no_wides.groupby('batting_position')['ball'].count().to_frame()
    outs = df['player_dismissed_pos'].value_counts().rename_axis('batting_position').to_frame('outs')
    innings_played = df.groupby('batting_position').match_id.nunique()
    runs_scored.reset_index(inplace=True)
    balls_faced.reset_index(inplace=True)
    outs.reset_index(inplace=True)
    outs = outs.rename(columns={'index': 'batting_position'})
    outs = outs[outs.batting_position != "-1"]
    batting_data = pd.merge(
        pd.merge(pd.merge(runs_scored, balls_faced, how="inner", on='batting_position'), outs, how="inner",
                 on='batting_position'), innings_played, how="inner", on='batting_position')
    batting_data['Batting Average'] = batting_data['runs_off_bat'] / batting_data['outs']
    batting_data['Batting Strike Rate'] = batting_data['runs_off_bat'] * 100 / batting_data['ball']
    batting_data.rename(columns={'batting_position': 'Player', 'runs_off_bat': 'Runs Scored', 'ball': 'Balls Faced',
                                 'outs': 'Times Dismissed', 'match_id': 'Innings Played'}, inplace=True)
    return batting_data
