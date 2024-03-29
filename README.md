# Spotify etl 
This repository aims to build your own Spotify Wrapped. It uses [Spotify Web API](https://developer.spotify.com/documentation/web-api) to retrieve your information and plotting it with [Shiny](https://shiny.posit.co/py/).

My own wrapped is available here [https://luismerinoulizarna.shinyapps.io/my-music-wrapped/](https://luismerinoulizarna.shinyapps.io/my-music-wrapped/)

# Usage
* Obtain your own Access Token from Spotify [here](https://developer.spotify.com/documentation/web-api/concepts/access-token)
  *  Store this token in a `.env` file.
* Run `pip install -r requirements.txt` to install all required requirements for the project.
* Under `~/dashboard` run `shiny run --reload --launch-browser ./app.py`

