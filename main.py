import sqlite3
import pandas as pd
import requests
import datetime
import sqlalchemy

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

USER_ID = "luismerino"  # your Spotify username

TOKEN = ("BQBwVSkMze5vYEmILB02k07GVfy2FODB982_dkVDOibYLDBCjieVAdSPXWjTcevVhp1t1MSmdYoi58zjhU9drI0wCA0CBWkwGytJMVgnhN6Z8eE5yYcOhMgbEM6ORrBmsfLUwsWFmP-X2sFzAVozaWJ44TTqQL13gRTUvc8kWtYz5Kg_lz6Zfh--87p7GD5yUKx06-F6bBYGOXT-8JuYVElMa80pQnhDEh5zdytXmcwOOmy8WifbH2IF2A")


def get_recently_played_after_time(my_time, headers):
    return requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=my_time),
        headers=headers)


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


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
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
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
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
