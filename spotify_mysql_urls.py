import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="df76a025d6e84e2cbce45d4e62dca200",
    client_secret="670e25194261425888d7b392346629ec"
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'spotify_database'
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read track URLs from file
file_path = "track_urls.txt"
with open(file_path, 'r') as file:
    track_urls = file.readlines()

# Process each URL
for track_url in track_urls:
    track_url = track_url.strip()  # Remove any leading/trailing whitespace
    print(f"Processing URL: {track_url}")  # Debug print

    try:
        # Extract track ID from URL
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)
        print(f"Track ID: {track_id}")  # Debug print

        # Fetch track details from Spotify API
        track = sp.track(track_id)
        print(f"Track details: {track}")  # Debug print

        # Extract metadata
        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

        # Confirm metadata extraction
        print(f"Track Data Extracted: {track_data}")  # Debug print

        try:
            # Insert data into MySQL
            print("Inserting data into MySQL...")  # Debug print
            insert_query = """
            INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                track_data['Track Name'],
                track_data['Artist'],
                track_data['Album'],
                track_data['Popularity'],
                track_data['Duration (minutes)']
            ))
            connection.commit()
            print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

        except Exception as e:
            print(f"Error inserting data: {e}")

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

# Close the connection
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")
