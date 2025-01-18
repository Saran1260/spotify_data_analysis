from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re

sp= spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="df76a025d6e84e2cbce45d4e62dca200",
    client_secret="670e25194261425888d7b392346629ec"
))

track_url="https://open.spotify.com/track/0Vh3jGxKhm9KxzQgnfnIV6"
track_id=re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

track=sp.track(track_id)
print(track)

track_data={
    'track name': track['name'],
    'artist':track['artists'][0]['name'],
    'album':track['album']['name'],
    'popularity':track['popularity'],
    'duration(minutes)':track['duration_ms'] / 60000
}

print(f"\n trackname:{track_data['track name']}")
print(f"artist:{track_data['artist']}")
print(f"album:{track_data['album']}")
print(f"popularity:{track_data['popularity']}")
print(f"duration:{track_data['duration(minutes)']:.2f} minutes")

df=pd.DataFrame([track_data])
print("\ntrack data as dataframe")
print(df)

df.to_csv('spotify_track_data.csv',index=False)

features=['popularity','duration(minutes)']
values=[track_data['popularity'],track_data['duration(minutes)']]

plt.figure(figsize=(8,5))
plt.bar(features,values,color='blue',edgecolor='black')
plt.title(f"track medata for '{track_data['track name']}'")
plt.ylabel('value')
plt.show()