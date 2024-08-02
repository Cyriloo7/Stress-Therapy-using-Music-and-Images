from src.logger.logger import logger
import sys
import pandas as pd
from src.exceptions.exception import customexception
from nltk.stem import WordNetLemmatizer
import mlflow


class PhobiaWordsCleaning:
    def __init__(self):
        logger.info("PhobiaWordsCleaning started")
        # Load phobia data from CSV
        self.dat = pd.read_csv("data/phobia_new.csv")
        # Create phobia dictionary
        self.phobias = {}
        for index, row in self.dat.iterrows():
            phobia = row["PHOBIAS"]
            related_words = self.preprocess_text(row["RELATED WORDS"])
            self.phobias[phobia] = related_words

        # Create phobia dictionary (lowercase all keys)
        phobias = {
            row["PHOBIAS"].lower(): self.preprocess_text(row["RELATED WORDS"])
            for index, row in self.dat.iterrows()
        }

        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        return [word.lower() for word in text.split(",") if word.isalpha()]

    def preprocess_phobia_words(self, prompt, phobia):
        try:
            logger.info("preprocess_phobia_words started")
            # If the user has a phobia, process the prompt
            if phobia:

                # Check if the phobia is in the dictionary
                if phobia in self.phobias:
                    related_words = self.phobias[phobia]
                    words_to_replace = ""
                    # Loop through each related word
                    for word in related_words:
                        # Lemmatize the related word
                        lemma = self.lemmatizer.lemmatize(word)

                        # Find all words in the prompt that have the same lemma
                        words_to_replace = [
                            w
                            for w in prompt.split()
                            if self.lemmatizer.lemmatize(w.lower()) == lemma
                        ]
                        for w in words_to_replace:
                            prompt = prompt.replace(w, " ")
                logger.info("phobia words to replaced and returned")
                mlflow.log_metrics("phobia words to replaced", prompt)
                return prompt
            else:
                print("No phobia entered.")
                logger.info("no phobia entered")
                return prompt
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)


"""        
if __name__ == "__main__":
    obj = PhobiaWordsCleaning()
    print(obj.preprocess_phobia_words("dark night full of darkness", "Achluophobia"))"""
