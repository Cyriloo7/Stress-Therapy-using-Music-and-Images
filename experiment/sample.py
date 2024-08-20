import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Replace with your own credentials
client_id = "2f495710f7854b099382a20ae7d6cc87"
client_secret = "1157403c5e6c4f70abe329eff142721f"
redirect_uri = "http://localhost:8080/callback"
scope = "user-read-playback-state user-modify-playback-state"

# Set up the Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri,scope=scope)

# Authenticate and get an access token
token_info = sp_oauth.get_access_token(as_dict =False)
print(token_info)
# Create a Spotify client object
sp_client = spotipy.Spotify(auth=token_info)

# Search for a song
song_name = "Speak to Me"  # Replace with the song you want to play
artist_name = "Pink Floyd"  # Replace with the artist of the song

result = sp_client.search(q=f"track:{song_name} artist:{artist_name}", type="track")

track_id = result['tracks']['items'][0]['id']
sp_client.start_playback(uris=[f"spotify:track:{track_id}"])