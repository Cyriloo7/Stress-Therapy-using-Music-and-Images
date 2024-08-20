import os
import sys
import pandas as pd
import spotipy
import cv2
import time
from spotipy.oauth2 import SpotifyOAuth
from src.logger.logger import logger
from src.exceptions.exception import customexception

class SpotifySongStream:
    def __init__(self):
        try:
            logger.info("SpotifySongStream started")
            self.client_id = "2f495710f7854b099382a20ae7d6cc87"
            self.client_secret = "1157403c5e6c4f70abe329eff142721f"
            self.redirect_uri = "http://localhost:8080/callback"
            self.scope = "user-read-playback-state user-modify-playback-state"

            self.sp_oauth = SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri,scope=self.scope)

            # Get access token
            self.token_info = self.sp_oauth.get_access_token(as_dict =False)
            logger.info("self.token_info collected: %s", self.token_info)
        except Exception as e:
            logger.error(customexception(e, sys))
            raise customexception(e, sys)

    def pause_song(self):
        try:
            logger.info("Pausing song")
            if not self.token_info or "access_token" not in self.token_info:
                raise customexception("Invalid or missing access token", sys)

            sp = spotipy.Spotify(auth=self.token_info)
            sp.pause_playback()
            print("Playback paused successfully.")
        except spotipy.exceptions.SpotifyException as e:
            logger.error(f"Error pausing playback: {e}")
        except Exception as e:
            logger.error(customexception(e, sys))
            raise customexception(e, sys)

    def stream_song(self, random_song, directory_name):
        try:
            sp_client = spotipy.Spotify(auth=self.token_info)
            artist_name = random_song["Name"]
            song_title = random_song["Track Name"]
            duration = random_song["Duration ms"]

            result = sp_client.search(
                q=f"track:{song_title} artist:{artist_name}", type="track"
            )

            if result and result.get("tracks") and result["tracks"].get("items"):
                track_id = result["tracks"]["items"][0]["id"]
                sp_client.start_playback(uris=[f"spotify:track:{track_id}"])

                image_files = os.listdir(directory_name)
                for image_file in image_files:
                    try:
                        image_path = os.path.join(directory_name, image_file)
                        display = cv2.imread(image_path)
                        if display is not None:
                            cv2.imshow("window", display)
                            cv2.waitKey(int(duration // len(image_files)))
                            cv2.destroyAllWindows()
                        else:
                            logger.warning(f"{image_path} not found.")
                    except Exception as e:
                        logger.error(f"Error displaying image {image_path}: {e}")
                        raise customexception(e, sys)
                time.sleep(1)
            else:
                logger.warning("No tracks found for the given query.")
                return "No tracks found for the given query."

        except Exception as e:
            logger.error(customexception(e, sys))
            raise customexception(e, sys)

if __name__ == "__main__":
    spotify_song_stream = SpotifySongStream()
    random_song = pd.read_csv('data/new_file.csv')
    random_song = random_song.sample(1)
    spotify_song_stream.stream_song(random_song, r"C:\Users\cyril\Documents\GitHub\Stress-Therapy-using-Music-and-Images\artifacts\Generated image\Generated_image_1723953001")
    #spotify_song_stream.pause_song()
