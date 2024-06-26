from pathlib import Path

import pandas as pd
import seaborn as sns

from shiny import reactive
from shiny.express import input, render, ui
from faicons import icon_svg as icon

sns.set_theme(style="white")
df = pd.read_csv(Path(__file__).parent / "my_played_songs.csv", na_values="NA")
artists = [artist for artist in df["artist_name"].unique()]
dates = sorted([date for date in df["timestamp"].unique()], reverse=True)
print(df)


def count_songs(data_frame: pd.DataFrame) -> int:
    return data_frame["song_name"].shape[0]


def count_songs_by_artist(data_frame: pd.DataFrame, artist: str) -> int:
    return data_frame[data_frame["artist_name"] == artist].shape[0]


def count_artist(data_frame: pd.DataFrame) -> int:
    return data_frame["artist_name"].unique().shape[0]


with ui.value_box(showcase=icon("clock-rotate-left")):
    "Period"
    f"From {df.iloc[0, 3]} to {df.iloc[df.shape[0] - 1, 3]}"

with ui.layout_columns():
    with ui.value_box(showcase=icon("spotify")):
        "Total artists"
        count_artist(df)

    with ui.value_box(showcase=icon("music")):
        "Total songs"
        count_songs(df)

with ui.sidebar():
    ui.input_checkbox_group("artists", "Filter by artist", artists, selected=artists)
    ui.input_checkbox_group("date", "Filter by date", dates, selected=dates[0])


@reactive.calc
def filtered_df() -> pd.DataFrame:
    filt_df = df[df["artist_name"].isin(input.artists())]
    filt_df = filt_df[filt_df["timestamp"].isin(input.date())]
    return filt_df


with ui.layout_columns():
    for index, artist in enumerate(artists):
        songs = count_songs_by_artist(df, artist)
        with ui.value_box(theme="primary", value=songs):
            artist
            exec(f"""
@render.text
def {artist.lower().replace(" ", "_")}_count():
    pass
""")

with ui.layout_columns():
    with ui.card():
        ui.card_header("Summary")


        @render.data_frame
        def summary_statistics():
            display_df = filtered_df()[
                [
                    "song_name",
                    "artist_name",
                    "timestamp"
                ]
            ]
            return render.DataGrid(display_df, filters=True)

    with ui.card():
        ui.card_header("Artists throughout time")


        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="artist_name",
                y="timestamp",
                hue="artist_name",
            )
