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
        if (df['match_id'][i] == df['match_id'][i - 1] and df['innings'][i] == df['innings'][i - 1]):
            if (not (math.isnan(df['wides'][i - 1]))) or (
                    not math.isnan(df['noballs'][i - 1])):
                df['ball'][i] = df['ball'][i - 1]
            elif (math.floor(df['ball'][i]) == math.floor(df['ball'][i - 1])):
                df['ball'][i] = round(df['ball'][i - 1] + .1, 1)
                if (round(df['ball'][i] - math.floor(df['ball'][i]), 1) > 0.6):
                    curi = i
                    while (df['ball'][curi] > math.floor(df['ball'][i]) and not df['legbyes'][curi] > 0):
                        df['ball'][curi] = round(df['ball'][curi] - .1, 1)
                        curi -= 1
    return df
