from src.logger.logger import logger
import sys
import pandas as pd
from src.exceptions.exception import customexception
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer


class SongRecommentation:
    def __init__(self):
        logger.info("SongRecommentation class initialized")
        self.label_encoder = LabelEncoder()
        # Load the song dataset
        self.df = pd.read_csv("data/new_file.csv")
        self.df = self.df.dropna()
        self.df1 = self.df.copy()
        #self.df1 = self.df1.drop(['Unnamed: 0'], axis=1)
        self.df = self.df.drop(["Name", 'Track Name', 'Unnamed: 0',"Spotify URL"], axis=1)
        self.df['Genres'] = self.label_encoder.fit_transform(self.df['Genres'])
        self.processed_data = self.df
        

    def preprocess_recommender_data(self, data):
        try:
            data['Genres'] = self.label_encoder.fit_transform(data['Genres'])
            return data
        except Exception as e:
            raise customexception(e, sys)

    def kNN_song_recommender(self, input_features):
        try:
            num_recs=len(self.df)
            logger.info("kNN_song_recommender started")
            song_model = NearestNeighbors(n_neighbors=num_recs, metric='cosine')
            song_model.fit(self.processed_data)
            input_features_df = pd.DataFrame(input_features, index=[0])
            _, indices = song_model.kneighbors(input_features_df.values)
            top_songs_index = indices[0]
            top_songs = self.df1.iloc[top_songs_index]
            logger.info("kNN_song_recommender finished")
            return top_songs
        except Exception as e:
            raise customexception(e, sys)
    
    def convert_input_feature(self, random_song):
        try:
            logger.info("Getting input feature started")
            # Accessing individual values directly from the pandas Series
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
            # Check if the genre exists in the label encoder
            if input_features['Genres'] not in self.label_encoder.classes_:
                logger.warning(f"Genre {input_features['Genres']} not found in label encoder. Using default value.")
                input_features['Genres'] = self.label_encoder.transform([self.label_encoder.classes_[0]])[0]
            else:
                input_features['Genres'] = self.label_encoder.transform([input_features['Genres']])
            logger.info("Getting input feature finished")
            return input_features
        except Exception as e:
            raise customexception(e, sys)
    
    def get_song_and_artist_info(self, random_song):
        logger.info("Getting song and artist info")
        try:
            input_features = {
                    'Track Name': random_song['Track Name'],
                    'Name': random_song['Name']
                    }
            return input_features
        except Exception as e:
            raise customexception(e, sys)


"""if __name__ =="__main__":
    obj = SongRecommentation()
    import pandas as pd
    random_song = pd.read_csv('data/new_file.csv')
    random_song = random_song.sample(1)
    random_song = obj.convert_input_feature(random_song)
    text = obj.kNN_song_recommender(random_song)
    print(text)"""

