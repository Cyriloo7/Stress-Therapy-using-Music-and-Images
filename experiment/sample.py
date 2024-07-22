import pandas as pd
random_song = pd.read_csv('data/new_file.csv')
random_song = random_song.sample(1)
print(random_song["Track Name"])