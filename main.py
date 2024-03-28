import os
import sqlite3
from datetime import datetime

import pandas as pd

from etl.transforms import check_if_valid_data, transform_input_data

from dotenv import load_dotenv

from utils.api import get_recently_played_after_time
from utils.date_utils import get_yesterday_unix, get_today, get_yesterday, get_today_human, get_yesterday_human
from etl.load import load_sqlLite
from etl.extract import extract_from_api


if __name__ == "__main__":
    load_dotenv()

    print(" ####### Extracting your masterpieces from Spotify... #######")

    response = get_recently_played_after_time(get_yesterday_unix())

    print(" ####### Extracted! Take a look to your last songs! #######")

    song_df = extract_from_api(response)
    print(song_df)

    data_to_save = transform_input_data(song_df)
    data_to_save.to_csv("dashboard/my_played_songs.csv")

    print("####### Data valid, proceed to Load stage #######")

    load_sqlLite(data_to_save, to_s3=True)


def get_df() -> pd.DataFrame:
    load_dotenv()
    return transform_input_data(extract_from_api(get_recently_played_after_time(get_yesterday_unix())))
