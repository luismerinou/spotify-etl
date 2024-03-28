from datetime import datetime

import pandas as pd
from utils.date_utils import get_yesterday, get_today, get_yesterday_human, get_today_human


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    if not pd.Series(df['played_at']).is_unique:
        raise KeyError(f"Primary Key is violated: {df['played_at']} is duplicated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception(f'Null values found: {df.isnull().values}')

    timestamps: list = df["timestamp"].tolist()
    not_yesterday: list = []
    for timestamp in timestamps:
        if datetime.strptime(timestamp, '%Y-%m-%d').day != get_yesterday().day:
            not_yesterday.append(timestamp)

    if not is_empty(not_yesterday):
        raise Exception(
            "####### Data invalid, probably not containing data only from yesterday {}\n but today is {}, not loaded "
            "to any"
            "data storage system #######".format(get_yesterday_human(), get_today_human()))

    return is_empty(not_yesterday)


def transform_input_data(df: pd.DataFrame) -> pd.DataFrame:
    if check_if_valid_data(df):
        return df
    else:
        raise Exception("####### Unexpected invalid data ######")


def is_empty(my_list: list) -> bool:
    return len(my_list) == 0
