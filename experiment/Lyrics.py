import lyricsgenius
from requests.exceptions import Timeout
import time
from langdetect import detect, LangDetectException
from googletrans import Translator

client_access_token = "UxedcM-g8B3Z0SLMKXGyOkqEwHanXlRXNs0lvw0aYAPgO72W9YRRrogK5c165BJe"
genius = lyricsgenius.Genius(client_access_token, timeout=10)  # Increase timeout to 10 seconds
genius.remove_section_headers = True

translator = Translator()

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

def translate_to_english(text):
    try:
        translated = translator.translate(text, src='auto', dest='en')
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def song_Lyrics(artist_name, song_title, retries=3):
    for attempt in range(retries):
        try:
            song = genius.search_song(song_title, artist_name)
            if song:
                lyrics = song.lyrics
                if is_english(lyrics):
                    print(lyrics)
                    return lyrics
                else:
                    print("The lyrics are not in English. Translating...")
                    translated_lyrics = translate_to_english(lyrics)
                    print(translated_lyrics)
                    return translated_lyrics
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
    

try:
    artist_name = "Wiz Khalifa"
    song_title = "See You Again"
    text = song_Lyrics(artist_name, song_title)
except Exception as e:
    print(f"An error occurred: {e}")