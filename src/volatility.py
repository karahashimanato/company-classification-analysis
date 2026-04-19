import numpy as np

def calc_log_returns(price_df):
    return_df = np.log(price_df / price_df.shift(1))
    return return_df


def calc_rolling_volatility(return_df, window=30, annualize=True):
    rolling_vol = return_df.rolling(window).std() * np.sqrt(252)
    return rolling_vol