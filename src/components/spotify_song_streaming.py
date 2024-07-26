from src.logger.logger import logger
import sys
import pandas as pd
from src.exceptions.exception import customexception
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2
import requests
import time
#import jsonify

class SpotifySongStream:
    def __init__(self):
        logger.info("SpotifySongStream started")
        self.sp_oauth = SpotifyOAuth(
            client_id='e8039d95de6b49b5b89e632a200ef84f',
            client_secret='84bd96017624467c8096c2ab1b8588a9',
            redirect_uri='http://localhost:8080/callback',
            scope='user-read-playback-state,user-modify-playback-state'
        )
        self.token_info = self.get_token_info()
        self.sp_client = spotipy.Spotify(auth=self.token_info['access_token'])
    
    def get_token_info(self):
        # Handling the deprecation warning
        try:
            token_info = self.sp_oauth.get_cached_token()
            if not token_info:
                token_info = self.sp_oauth.get_access_token(as_dict=False)
            return token_info
        except Exception as e:
            print(f"Error obtaining token: {e}")
            return None
    
    def get_current_playing_track(self):
        try:
            track_url = 'https://api.spotify.com/v1/me/player/currently-playing'
            headers = {
                'Authorization': f'Bearer {self.token_info["access_token"]}'
            }
            response = requests.get(track_url, headers=headers)
            if response.status_code == 200:
                track_data = response.json()
                if track_data:
                    track_name = track_data['item']['name']
                    artist_name = track_data['item']['artists'][0]['name']
                    print(f"Currently playing: {track_name} by {artist_name}")
                    self.pause_song()
                    return True
                else:
                    print("No track is currently playing.")
                    return False
            else:
                print(f"Failed to get currently playing track: {response.status_code}")
        except Exception as e:
            logger.error(f"Error getting currently playing track: {e}")
            logger.info(customexception(e, sys))
            raise customexception(e, sys)


    def pause_song(self):
        try:
            logger.info("pausing song")
            try:
                sp = spotipy.Spotify(auth=self.token_info['access_token'])
                sp.pause_playback()
                print("Playback paused successfully.")
            except spotipy.exceptions.SpotifyException as e:
                print(f"Error pausing playback: {e}")
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
        
    
    def stream_song(self, random_song):
        try:
            artist_name = random_song['Name']  # Use .values[0] to get the value from the DataFrame
            song_title = random_song['Track Name']
            logger.info("Streaming song")
            duration = random_song["Duration ms"] # Use .values[0] to get the value from the DataFrame

            result = self.sp_client.search(q=f"track:{song_title} artist:{artist_name}", type="track")

            if not result['tracks']['items']:
                print("No tracks found for the given query.")
                return

            track_id = result['tracks']['items'][0]['id']
            self.sp_client.start_playback(uris=[f"spotify:track:{track_id}"])

            for i in range(4):
                display = cv2.imread(f'artifacts/Generated image/Generated_image{i}.jpg')
                if display is not None:
                    cv2.imshow('window', display)
                    cv2.waitKey(int(duration // 4))
                    cv2.destroyAllWindows()
                else:
                    logger.warning(f"Image artifacts/Generated image/Generated_image{i}.jpg not found.")

            """try:
                self.sp_client.pause_playback()
                print("Playback paused successfully.")
            except spotipy.exceptions.SpotifyException as e:
                print(f"Error pausing playback: {e}")
            logger.info("Playback paused successfully.")"""
            time.sleep(1)

        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)

        



"""if __name__ == "__main__":
    spotify_song_stream = SpotifySongStream()
    print(spotify_song_stream.get_current_playing_track())
    random_song = pd.read_csv('data/new_file.csv')
    random_song = random_song.sample(1)
    #spotify_song_stream.stream_song(random_song)
    spotify_song_stream.pause_song()"""