import datetime
import os
import sqlite3

import pandas as pd
import requests
import sqlalchemy

from utils.transforms import check_if_valid_data

from dotenv import load_dotenv

from utils.date_utils import get_yesterday_unix


def get_recently_played_after_time(my_time, headers):
    return requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=my_time),
        headers=headers)


if __name__ == "__main__":
    load_dotenv()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=os.getenv("TOKEN"))
    }

    print(" ####### Extracting your masterpieces from Spotify... #######")
    try:
        request = get_recently_played_after_time(get_yesterday_unix(), headers)
        response = request.json()
    except Exception:
        raise Exception("Error while fetching data, check your access token, request headers and request parameters")

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

    print("****** Starting load process ******")
    engine = sqlalchemy.create_engine(os.getenv("DATABASE_CONNECTION"))
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """
    try:
        cursor.execute(sql_query)
        print("Opened database successfully")
    except Exception:
        raise Exception("Error while executing SQL query")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except Exception:
        raise Exception("Data already exists in the database")

    try:
        conn.close()
        print("Close database successfully")
    except Exception:
        raise Exception("Error while closing the connection to the database")
