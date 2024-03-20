import os

import requests


def get_recently_played_after_time(unix_date: int) -> requests.Response:
    TOKEN = ("BQB-AQcVxuZ1-ls_EIc1OwPnjF4j1sJPa5fhujvrHEJcOvqhEnZlQmCbrikXc2gAStCDFkEEH5_40WgTV6NbcOe-4RXYgh7-Tab"
             "-vftocY15zY-aMtsE0eb3lrPAiUfLJi_jHL20GpXWZIa_tv09sOEevWGt3nBwitoY1SPjlvdU7s6Z3atRN35CDcrUjfOZ0LFvdu_5D4CmQsOyGoDpus47-WK5yF_Y7XnP9nUEs4ESTQS78MvZmaO8jQ")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=get_token())
    }
    try:
        response: requests.Response = requests.get(
            "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=unix_date),
            headers=headers).json()
        return response
    except requests.exceptions.HTTPError as err:
        if err == 401:  # Token expired
            Exception("Token expired. Refresh it and retry")
        else:
            print(f"HTTP Error: {err}")
    except Exception as e:
        # Handle other exceptions
        Exception(f"An error occurred: {e}")


def get_token() -> str:
    return os.getenv("TOKEN")
