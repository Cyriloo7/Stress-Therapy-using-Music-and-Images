#
#
# Profinity words are added in negative words list in json file
#
# 

import nltk
from nltk.corpus import wordnet
import json
import sys
from src.exceptions.exception import customexception
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
            logger.error("The file was not found.")
            words_list = {'positive_words': [], 'negative_words': []}
        except json.JSONDecodeError:
            logger.error("Error decoding JSON. Please check the file format.")
            words_list = {'positive_words': [], 'negative_words': []}
        
        self.positive_words = set(word.lower() for word in words_list['positive_words'])
        self.negative_words = set(word.lower() for word in words_list['negative_words'])
        logger.info("Profanity JSON file loaded successfully")
    
    def get_antonym(self, word):
        logger.info("Antonym checking started")
        antonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())
        logger.info("Antonym checking finished")
        return antonyms[0] if antonyms else word
    
    def initiate_profanity_check(self, sentence):
        try:
            logger.info("Initiate profanity check started")
            self.words = sentence.split()
            transformed_words = [self.get_antonym(word.lower()) if word.lower() in self.negative_words else word for word in self.words]
            logger.info("Initiate profanity check finished")
            return ' '.join(transformed_words)
        except Exception as e:
            raise customexception(e, sys)

if __name__ == "__main__":
    obj = Profanity()
    print(obj.initiate_profanity_check("sex to it and do good and bad"))








