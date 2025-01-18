import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

sp= spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="df76a025d6e84e2cbce45d4e62dca200",
    client_secret="670e25194261425888d7b392346629ec"
))

db_config={
    'host':'localhost',
    'user':'root',
    'password':'admin',
    'database':'spotify_database'
}

connection=mysql.connector.connect(**db_config)
cursor=connection.cursor()

track_url="https://open.spotify.com/track/0Vh3jGxKhm9KxzQgnfnIV6"

track_id=re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

track=sp.track(track_id)

track_data={
    'track name': track['name'],
    'artist':track['artists'][0]['name'],
    'album':track['album']['name'],
    'popularity':track['popularity'],
    'duration(minutes)':track['duration_ms'] / 60000
}

insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""


cursor.execute(insert_query,(
    track_data['track name'],
    track_data['artist'],
    track_data['album'],
    track_data['popularity'],
    track_data['duration(minutes)']
))

connection.commit()

print(f"track'{track_data['track name']}'by{track_data['artist']}inserted into database.")

cursor.close()
connection.close()