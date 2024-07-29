import os
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
        
    
    def stream_song(self, random_song, directory_name):
        try:
            sp_client = spotipy.Spotify(auth=self.token_info['access_token'])
            artist_name = random_song['Name']  # Use .values[0] to get the value from the DataFrame
            song_title = random_song['Track Name']
            logger.info("Streaming song")
            duration = random_song["Duration ms"] # Use .values[0] to get the value from the DataFrame

            result = sp_client.search(q=f"track:{song_title} artist:{artist_name}", type="track")

            if not result['tracks']['items']:
                print("No tracks found for the given query.")
                return "No tracks found for the given query."

            track_id = result['tracks']['items'][0]['id']
            sp_client.start_playback(uris=[f"spotify:track:{track_id}"])

            no_of_images = os.listdir(directory_name)
            for i in no_of_images:
                try:
                    image_path = os.path.join(directory_name, i)
                    display = cv2.imread(image_path)
                    if display is not None:
                        cv2.imshow('window', display)
                        cv2.waitKey(int(duration // len(no_of_images)))
                        cv2.destroyAllWindows()
                    else:
                        logger.warning(f"{directory_name}/{i} not found.")
                except Exception as e:
                    logger.error(f"{directory_name}/{i} not found.")
                    raise customexception(e, sys)

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