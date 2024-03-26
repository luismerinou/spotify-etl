import boto3
import sqlalchemy
import sqlite3
import os
import pandas as pd


def load_sqlLite(data_frame_to_save: pd.DataFrame, to_s3: bool = False):
    print("****** Starting load process ******")
    engine = sqlalchemy.create_engine(os.getenv("DATABASE_CONNECTION"))
    sqlite = 'my_played_tracks.sqlite'
    conn = sqlite3.connect(sqlite)
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
        data_frame_to_save.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except Exception:
        raise Exception("Data already exists in the database")

    try:
        conn.close()
        print("Close database successfully")
    except Exception:
        raise Exception("Error while closing the connection to the database")

    if to_s3:
        load_to_s3("/Users/luismerinoulizarna/PycharmProjects/spotify-api-etl/my_played_tracks.sqlite")


def load_to_s3(path):
    s3 = boto3.client('s3')
    s3.upload_file(path, 'spotify-api-etl', 'database.sqlite')
