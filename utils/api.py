import os

import requests
# from utils.auth import get_token


def get_recently_played_after_time(unix_date: int) -> requests.Response:
    # token = get_token()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=os.getenv("TOKEN"))
    }
    response: requests.Response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=unix_date),
        headers=headers).json()

    return response

