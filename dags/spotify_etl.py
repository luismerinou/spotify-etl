import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
import logging


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

        # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Check that all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True


def get_recently_played_after_time(my_time, headers):
    return requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=my_time),
        headers=headers)


def run_spotify_etl():
    logger = logging.getLogger(__name__)

    database_location = "sqlite:///my_played_tracks.sqlite"

    user_id = "luismerino"  # your Spotify username

    token = (
        "BQBXYU8DK2LZZt1EJI02cwYvKL6nYE3S2_OTCuZy49MFyrZci7a8d7JpTSM6PUGM1HIq-giOLYqxskqnr0XLYhMd4LVIE"
        "-wuKjv0IqA1pp61l9mpcMupkKU3BdMvBsTfHFD-1svmggtXgzDMrCaMWJioqVqPwYzP39dYrsaZRiQrsFNK5NUvRx46iOor1_v0XKwPbFJ"
        "-kvmYx6FXiSU5Llo1KLQ2aBR7etOsbh5n_gVmhBsf_fXZXp-WvQ")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=token)
    }

    # Convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours
    print(" ####### Extracting your masterpieces from Spotify... #######")
    try:
        request = get_recently_played_after_time(yesterday_unix_timestamp, headers)
        response = request.json()
    except Exception:
        raise Exception("Error while fetching data, check your access token, request headers and request parameters")

    print(" ####### Extracted! Take a look to your last songs! #######")

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Relevant fields only
    for song in response["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

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
    engine = sqlalchemy.create_engine(database_location)
    logger.info(f"connected to engine {engine}")
    conn = sqlite3.connect('my_played_tracks.sqlite')
    logger.info(f"connected to DB {str(conn)}")
    cursor = conn.cursor()
    logger.info(f" Load cursor {cursor}")

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
        logger.info(f" Executing QUERY {cursor.execute(sql_query)}")
        print("Opened database successfully")
    except Exception:
        logger.info("Error while executing SQL query")
        raise Exception("Error while executing SQL query")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
        logger.info("Created song df to sql")

    except Exception:
        logger.info("!!!! [LOG] Data already exists in the database [LOG]")
        raise Exception("Data already exists in the database")

    try:
        conn.close()
        print("Close database successfully")
    except Exception:
        raise Exception("Error while closing the connection to the database")
