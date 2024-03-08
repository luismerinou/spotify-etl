import pandas as pd
import requests
import datetime

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

USER_ID = "luismerino"  # your Spotify username

TOKEN = ("BQAs0iYOkQeQmRJxBLWgsO4vZOKwZb6gsVJzniKGhr7TfpIgSl8xyfihRLs3lwn3CyTPyDOg2CzId0ml_23_by"
         "-xU5Jyj0v3FLjwrpQ9sywdVABLNhKiqOacBNiqAfijo54NVRLG_pln0tTem_7O00q7-a55Kc8"
         "-Wg_nyEP201kin87TxImdSObj4Pxe1Izdac4meFtaVWrxOqKbiXVBfRW9YE0TTLtKefiXPECvSftZFX0ZkONhBzbU7Q")


def get_recently_played_after_time(my_time, headers):
    return requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)


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
    request = get_recently_played_after_time(yesterday, headers)
    response = request.json()

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
