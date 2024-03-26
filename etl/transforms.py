from datetime import datetime

import pandas as pd
from utils.date_utils import get_yesterday, get_today


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    if not pd.Series(df['played_at']).is_unique:
        raise KeyError(f"Primary Key is violated: {df['played_at']} is duplicated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception(f"Null values found: {df.isnull().values}")

    timestamps: list = df["timestamp"].tolist()
    not_yesterday: list = []
    for timestamp in timestamps:
        if datetime.strptime(timestamp, '%Y-%m-%d') != get_yesterday():
            not_yesterday.append(timestamp)
           # raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return is_empty(not_yesterday)


def is_empty(my_list: list) -> bool:
    return len(my_list) < 0
