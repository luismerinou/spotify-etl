import os
import sqlite3

import pandas as pd

from etl.transforms import check_if_valid_data

from dotenv import load_dotenv

from utils.api import get_recently_played_after_time
from utils.date_utils import get_yesterday_unix
from etl.load import load_sqlLite


if __name__ == "__main__":
    load_dotenv()

    print(" ####### Extracting your masterpieces from Spotify... #######")

    response = get_recently_played_after_time(get_yesterday_unix())

    print(" ####### Extracted! Take a look to your last songs! #######")

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    try:
        # Relevant fields only
        for song in response["items"]:
            song_names.append(song["track"]["name"])
            artist_names.append(song["track"]["album"]["artists"][0]["name"])
            played_at_list.append(song["played_at"])
            timestamps.append(song["played_at"][0:10])
    except KeyError:
        raise KeyError("Items not found, check if your Spotify Access Token has expired and retry")

    # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    print(song_df)

    if check_if_valid_data(song_df):
        print("####### Data valid, proceed to Load stage #######")
        load_sqlLite(song_df, to_s3=True)
    else:
        print("Invalid data")



