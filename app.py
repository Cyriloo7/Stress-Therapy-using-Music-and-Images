import random
from flask import Flask, jsonify, render_template, request
from src.components.convert_to_positive_sentence import Profanity
from src.components.divide_into_4parts import DivideInToFourParts
from src.components.lyrics_extractor import LyricsExtractor
from src.components.phobia_words_cleaning import PhobiaWordsCleaning
from src.components.song_recommentation import SongRecommentation
from src.components.spotify_song_streaming import SpotifySongStream
from src.components.stress_detection import StressDetection
from src.components.text_summarization import TextSummarizer
from src.components.text_to_image_generator import TextToImage
from src.exceptions.exception import customexception
from src.logger.logger import logger
import pandas as pd
import sys
import threading
import time
import torch
import mlflow

Profanity = Profanity()
DivideInToFourParts = DivideInToFourParts()
LyricsExtractor = LyricsExtractor()
PhobiaWordsCleaning = PhobiaWordsCleaning()
SongRecommentation = SongRecommentation()
SpotifySongStream = SpotifySongStream()
StressDetection = StressDetection()
TextSummarizer = TextSummarizer()
TextToImage = TextToImage()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = pd.read_csv("data/new_file.csv")

# Shared variable and a lock
lock = threading.Lock()
stop_thread_two_event = threading.Event()

app = Flask(__name__)

stress_detected = False
input_feature = None
random_song = None
song_finished = False
phobia = ""

def thread_one(j_file, js_file, input_features): # detection thread
    logger.info("Thread 1 started")
    global stress_detected
    global random_song
    global phobia
    count = 1
    c=0
    while True:
        c=c+1
        try:
            if count/20000==0:
                prediction = StressDetection.detect_stress(j_file)
            else:
                prediction = StressDetection.detect_stress(js_file)
            if prediction[0] != 0:  # Assuming 1 indicates stress
                with lock:
                    stress_detected = True
                    print("Stress detected", prediction)
                    logger.info("Stress detected")
                    SpotifySongStream.pause_song()
                    recommended_songs = SongRecommentation.kNN_song_recommender(input_features)
                    random_song_index = random.randint(200, 7000)
                    print("random value ",random_song_index)
                    recommended_songs_list = recommended_songs.iloc[random_song_index] # Remove first 200 songs
                    if not recommended_songs_list.empty:
                        random_song = recommended_songs_list.iloc[random_song_index]
                        print("Playing new recommended song:", random_song['Track Name'])
                    else:
                        print("No more recommended songs.")
                        break
                time.sleep(50)    
                with lock:
                    stress_detected = False 
                    stop_thread_two_event.set()
                    time.sleep(50)
                    stop_thread_two_event.clear()
                    # Start a new thread two
                    t2 = threading.Thread(target=thread_two, args=(phobia,))
                    t2.start()               
        except Exception as e:
            raise customexception(e, sys)
        time.sleep(3)  # Check every 3 second

def thread_two(): # song recommendation, image generation, song streaming
    first_round = 0
    global song_finished
    global random_song
    global phobia
    while True:
        logger.info("Getting random song feature values...")
        input_feature = SongRecommentation.convert_input_feature(random_song)
        logger.info("Getting random song feature values finished")
        logger.info("getting song and artist information...")
        inform_song = SongRecommentation.get_song_and_artist_info(random_song)
        logger.info("Lyrics is extracting")
        lyrics = LyricsExtractor.song_Lyrics(inform_song)
        logger.info("Lyrics is extracting finished")
        logger.info("Profanity cleaninf started")
        profanity_clean_lyrics = Profanity.initiate_profanity_check(str(lyrics))
        logger.info("Text is summarizing")
        summary = TextSummarizer.first_summarize(profanity_clean_lyrics)
        logger.info("Text is summarizing finished")
        logger.info("Phobia words are cleaning")
        cleaned_lyrics = PhobiaWordsCleaning.preprocess_phobia_words(summary, phobia=phobia)
        logger.info("Phobia words are cleaning finished")
        logger.info("Text is divided into 4 parts")
        divided_lyrics = DivideInToFourParts.divide_into_four_parts(cleaned_lyrics)
        logger.info("Text is divided into 4 parts finished")
        """logger.info("The divided parts is again summarized")
        part_summary = []
        for i in range(4):
            part_summary.append(TextSummarizer.second_summarize(divided_lyrics[i]))
            logger.info(f"Part {i+1}: summarized")
        logger.info("Text is divided into 4 parts again summarized finished")"""

        logger.info("Generating image")
        directory_name = TextToImage.text_to_image(divided_lyrics)
        logger.info("Generating image finished")
        if first_round !=0:
            logger.info("Waiting for the song to finish...")
            t3.join()
        first_round = 1

        if stress_detected == False:
            logger.info("Stress not detected, streaming song")
            song_finished = False
            t3 = threading.Thread(target=thread_three, args=(random_song,directory_name))
            # Start thread three
            t3.start()
            song_finished = True 
            recommended_songs = SongRecommentation.kNN_song_recommender(input_feature)
            random_song_index = random.randint(1, 200)
            print("random value ", random_song_index)
            random_song = recommended_songs.iloc[random_song_index]
        else:
            time.sleep(10)
            pass

def thread_three(random_song,directory_name): # stream song
    SpotifySongStream.stream_song(random_song, directory_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global random_song
    global phobia
    with mlflow.start_run():
        mlflow.autolog()

        j_file = r"C:/Users/cyril/Downloads/flask inout json/flask inout json/time_pressure.json"
        js_file = r"C:/Users/cyril/Downloads/flask inout json/flask inout json/no_stress.json"

        phobia = request.form.get('text')
        
        # Get a random song from the dataset
        random_song_index = random.randint(0, 1000)
        print("random_song_index", random_song_index)
        random_song = data.iloc[random_song_index]
        input_feature = SongRecommentation.convert_input_feature(random_song)

        t1 = threading.Thread(target=thread_one, args=(j_file, js_file, input_feature))
        t2 = threading.Thread(target=thread_two, args=())

        # Start thread two
        t2.start()

        # Start thread one
        t1.start()
        
        # Wait for threads to complete
        t1.join()
        t2.join()

    mlflow.end_run()

if __name__ == '__main__':
    app.run(debug=False)
