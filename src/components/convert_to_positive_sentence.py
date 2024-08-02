#
#
# Profinity words are added in negative words list in json file
#
#

import re
import nltk
from nltk.corpus import wordnet
import json
import sys
from profanityfilter import ProfanityFilter
from src.exceptions.exception import customexception
from src.logger.logger import logger
import mlflow

# Ensure you have the WordNet data
nltk.download("wordnet")
pf = ProfanityFilter()


class Profanity:

    def __init__(self):
        logger.info("Profanity JSON file loading started")
        try:
            with open("./data/positive_negative_words.json", "r") as file:
                words_list = json.load(file)
        except FileNotFoundError:
            logger.error("The file was not found.")
            words_list = {"positive_words": [], "negative_words": []}
        except json.JSONDecodeError:
            logger.error("Error decoding JSON. Please check the file format.")
            words_list = {"positive_words": [], "negative_words": []}

        self.positive_words = set(word.lower() for word in words_list["positive_words"])
        self.negative_words = set(word.lower() for word in words_list["negative_words"])
        logger.info("Profanity JSON file loaded successfully")

        try:
            with open("./data/replacements.json", "r") as file:
                self.replacements = json.load(file)
        except FileNotFoundError:
            logger.error("The replacements file was not found.")
            self.replacements = {}
        except json.JSONDecodeError:
            logger.error(
                "Error decoding replacements JSON. Please check the file format."
            )
            self.replacements = {}

        logger.info("Profanity and replacements JSON files loaded successfully")

    def get_antonym(self, word):
        try:
            antonyms = []
            logger.info("get_antonym started")
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.antonyms():
                        antonyms.append(lemma.antonyms()[0].name())
            logger.info("get_antonym finished successfully")
            return antonyms[0] if antonyms else word
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)

    def filter_profanity(self, sentence):
        return pf.censor(sentence)

    def apply_replacements(self, sentence):
        for pattern, replacement in self.replacements.items():
            sentence = re.sub(pattern, replacement, sentence)
        return sentence

    def initiate_profanity_check(self, sentence):
        try:
            logger.info("Initiate profanity check started")
            sentence = self.apply_replacements(sentence)
            words = sentence.split()
            transformed_words = [
                (
                    self.get_antonym(word.lower())
                    if word.lower() in self.negative_words
                    else word
                )
                for word in words
            ]
            logger.info("Initiate profanity check finished")
            positive_sentence = " ".join(transformed_words)
            return self.filter_profanity(positive_sentence)
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)


"""if __name__ == "__main__":
    obj = Profanity()
    print(
        obj.initiate_profanity_check("sex to it and do good and bad I've got don't you")
    )
"""
