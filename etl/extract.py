import pandas as pd
import requests


def extract_from_api(response: requests.Response) -> pd.DataFrame:
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
    return song_df
