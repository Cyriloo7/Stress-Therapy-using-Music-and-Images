#
#
# Profinity words are added in negative words list in json file
#
# 

import nltk
from nltk.corpus import wordnet
import json
import sys
from src.logger.logger import logger

# Ensure you have the WordNet data
nltk.download('wordnet')


class Profanity:

    def __init__(self):
        logger.info("Profanity JSON file loading started")
        try:
            with open("./data/positive_negative_words.json", "r") as file:
                words_list = json.load(file)
        except FileNotFoundError:
            print("The file was not found.")
            words_list = {'positive_words': [], 'negative_words': []}
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            words_list = {'positive_words': [], 'negative_words': []}
            self.positive_words = set(word.lower() for word in words_list['positive_words'])
            self.negative_words = set(word.lower() for word in words_list['negative_words'])
        
        logger.info("Profanity JSON file loaded successfully")
        pass
    
    def get_antonym(self, word):
        logger.info("antonym checking started")
        antonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())
        logger.info("antonym checking finished")
        return antonyms[0] if antonyms else word
    
    def initiate_profanity_check(self, sentence):
        logger.info("initiate_profanity_check started")
        words = sentence.split()
        transformed_words = [self.get_antonym(word.lower()) if word.lower() in self.negative_words else word for word in words]
        logger.info("initiate_profanity_check finished")
        return ' '.join(transformed_words)


if __name__=="__main__":

    obj = Profanity()
    print(obj.initiate_profanity_check(obj, "sex to it and do goos nd bad"))






