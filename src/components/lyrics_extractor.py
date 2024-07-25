import lyricsgenius
from requests.exceptions import Timeout
import time
from tqdm import tqdm
from langdetect import detect, LangDetectException
from googletrans import Translator
import sys
import pandas as pd
from src.logger.logger import logger
from src.exceptions.exception import customexception
from google.cloud import translate_v3beta1 as translate


class LyricsExtractor:
    def __init__(self):
        logger.info("Initializing LyricsExtractor")
        self.client_access_token = "UxedcM-g8B3Z0SLMKXGyOkqEwHanXlRXNs0lvw0aYAPgO72W9YRRrogK5c165BJe"
        self.genius = lyricsgenius.Genius(self.client_access_token, timeout=10)  # Increase timeout to 10 seconds
        self.genius.remove_section_headers = True

        self.projectid = "deepfake-415910"
        self.targetlanguage = "en"

    def is_english(self, text):
        try:
            return detect(text) == 'en'
        except LangDetectException:
            return False

        
    def translate_text(self, text: str):
        client = translate.TranslationServiceClient()
        location = "global" 
        parent = f"projects/{self.projectid}/locations/{location}"

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "target_language_code": self.targetlanguage,
            }
        )

        translated_text = response.translations[0].translated_text
        detected_language_code = response.translations[0].detected_language_code


        return {
            "translated_text": translated_text,
            "detected_language_code": detected_language_code
        }

    def translate_to_english(self, text):
        result = self.translate_text(text)
        print("Translation to English was successful.")
        return result["translated_text"]

    def song_Lyrics(self, random_song, retries=3):
        logger.info(f"randon song: {random_song}")
        artist_name = random_song['Name']
        song_title = random_song['Track Name']
        for attempt in range(retries):
            try:
                if isinstance(song_title, pd.Series):
                    song_title = song_title.iloc[0] 
                if isinstance(artist_name, pd.Series):
                    artist_name = artist_name.iloc[0]
                song = self.genius.search_song(song_title, artist_name)
                if song:
                    lyrics = song.lyrics
                    if self.is_english(lyrics):
                        #print(lyrics.encode('utf-8', errors='replace').decode('utf-8'))
                        return lyrics.encode('utf-8')
                    else:
                        print("The lyrics are not in English. Translating...")
                        translated_lyrics = self.translate_to_english(lyrics)
                        #print(translated_lyrics.encode('utf-8', errors='replace').decode('utf-8'))
                        return translated_lyrics.encode('utf-8')
                else:
                    print("Song not found.")
                break
            except Timeout:
                if attempt < retries - 1:
                    print(f"Timeout occurred. Retrying {attempt + 1}/{retries}...")
                    time.sleep(2)  # Wait for 2 seconds before retrying
                else:
                    print("Failed to fetch artist data after multiple attempts.")
                    raise
            except Exception as e:
                raise customexception(e, sys)


"""
if __name__ =="__main__":
    obj = LyricsExtractor()
    import pandas as pd
    random_song = pd.read_csv('data/new_file.csv')
    random_song = random_song.sample(1)
    text = obj.song_Lyrics(random_song)
    print(text)
"""