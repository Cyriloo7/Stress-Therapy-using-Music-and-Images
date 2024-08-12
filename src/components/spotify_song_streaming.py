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


class SpotifySongStream:
    def __init__(self):
        logger.info("SpotifySongStream started")
        self.sp_oauth = SpotifyOAuth(
            client_id="e8039d95de6b49b5b89e632a200ef84f",
            client_secret="84bd96017624467c8096c2ab1b8588a9",
            redirect_uri="http://localhost:8080/callback",
            scope="user-read-playback-state,user-modify-playback-state",
        )
        self.token_info = self.get_token_info()

    def get_token_info(self):
        """
        Retrieves the access token for the Spotify API.

        This function attempts to retrieve the access token from the cached token or
        by requesting a new one from the Spotify OAuth server.

        Parameters:
        None

        Returns:
        dict: A dictionary containing the access token and other token information.
              If an error occurs during the retrieval process, returns None.
        """
        try:
            token_info = (
                self.sp_oauth.get_cached_token()
                or self.sp_oauth.get_access_token(as_dict=False)
            )
            return token_info
        except Exception as e:
            print(f"Error obtaining token: {e}")
            return None

    def pause_song(self):
        """
        Pauses the currently playing song on the Spotify account.

        This function uses the access token obtained from the get_token_info method to
        pause the playback on the Spotify account associated with the access token.

        Parameters:
        None

        Returns:
        None
        """
        try:
            logger.info("Pausing song")
            sp = spotipy.Spotify(auth=self.token_info["access_token"])
            sp.pause_playback()
            print("Playback paused successfully.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error pausing playback: {e}")
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)

    def stream_song(self, random_song, directory_name):
        """
        Streams a song from the Spotify API and displays images from a specified directory.

        This function takes a random song DataFrame and a directory name as input. It uses the
        access token obtained from the get_token_info method to interact with the Spotify API.
        It searches for the song in the Spotify library and starts playing it. Then, it displays
        images from the specified directory one by one, with a duration equal to the song's duration
        divided by the number of images.

        Parameters:
        random_song (pandas.DataFrame): A DataFrame containing information about a random song.
                                    It should have columns: "Name", "Track Name", and "Duration ms".
        directory_name (str): The name of the directory containing the images to be displayed.

        Returns:
        str: Returns "No tracks found for the given query." if no tracks are found for the given query.
            Otherwise, returns None.
        """
        try:
            sp_client = spotipy.Spotify(auth=self.token_info["access_token"])
            artist_name = random_song["Name"]
            song_title = random_song["Track Name"]
            logger.info("Streaming song")
            duration = random_song["Duration ms"]

            result = sp_client.search(
                q=f"track:{song_title} artist:{artist_name}", type="track"
            )

            if not result["tracks"]["items"]:
                logger.warning("No tracks found for the given query.")
                return "No tracks found for the given query."

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
                    logger.error(f"{image_path} not found.")
                    raise customexception(e, sys)
            time.sleep(1)

        except Exception as e:
            logger.error(customexception(e, sys))
            raise customexception(e, sys)


"""if __name__ == "__main__":
    spotify_song_stream = SpotifySongStream()
    print(spotify_song_stream.get_current_playing_track())
    random_song = pd.read_csv('data/new_file.csv')
    random_song = random_song.sample(1)
    spotify_song_stream.stream_song(random_song)
    spotify_song_stream.pause_song()
"""