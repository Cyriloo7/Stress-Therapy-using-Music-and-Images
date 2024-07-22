from src.logger.logger import logger
import sys
import pandas as pd
from src.exceptions.exception import customexception
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

class SongRecommentation:
    def __init__(self, dataset_path, num_recommendations):
        self.label_encoder = LabelEncoder()
        # Load the song dataset
        self.df = pd.read_csv("new_file.csv")
        #self.df1 = self.df.copy()
        #self.df1 = self.df1.drop(['Unnamed: 0'], axis=1)
        self.df = self.df.drop(["Name", 'Track Name', 'Unnamed: 0',"Spotify URL"], axis=1)
        

    def preprocess_recommender_data(self, data):
        data['Genres'] = self.label_encoder.fit_transform(data['Genres'])
        return data

    def kNN_song_recommender(self, processed_data, input_features, num_recs=len(self.df)):
        logger.info("kNN_song_recommender started")
        song_model = NearestNeighbors(n_neighbors=num_recs, metric='cosine')
        song_model.fit(processed_data)
        input_features_df = pd.DataFrame(input_features, index=[0])
        _, indices = song_model.kneighbors(input_features_df.values)
        top_songs_index = indices[0]
        top_songs = self.df.iloc[top_songs_index]
        logger.info("kNN_song_recommender finished")
        return top_songs
    
    def convert_input_feature(self, random_song):
        logger.info("Converting input feature started")
        input_features = {
            'Popularity': random_song['Popularity'],
            'Duration ms': random_song['Duration ms'],
            'Danceability': random_song['Danceability'],
            'Energy': random_song['Energy'],
            'Key': random_song['Key'],
            'Key Confidence': random_song['Key Confidence'],
            'Loudness': random_song['Loudness'],
            'Mode': random_song['Mode'],
            'Mode Confidence': random_song['Mode Confidence'],
            'Speechiness': random_song['Speechiness'],
            'Acousticness': random_song['Acousticness'],
            'Instrumentalness': random_song['Instrumentalness'],
            'Liveness': random_song['Liveness'],
            'Valence': random_song['Valence'],
            'Tempo': random_song['Tempo'],
            'Tempo Confidence': random_song['Tempo Confidence'],
            'Time Signature': random_song['Time Signature'],
            'Time Signature Confidence': random_song['Time Signature Confidence'],
            'Genres': random_song['Genres']
        }
        input_features['Genres'] = self.label_encoder.fit_transform([input_features['Genres']])
        logger.info("Converting input feature finished")
        return input_features











