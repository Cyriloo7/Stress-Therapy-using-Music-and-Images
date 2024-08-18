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
            
            # Check if prompt is None
            if prompt is None:
                logger.error("The prompt is None")
                return None
            
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
                            
                    logger.info("Phobia words replaced and returned")
                    return prompt
                else:
                    logger.info("Phobia not found in dictionary")
                    return prompt
            else:
                logger.info("No phobia entered")
                return prompt
                
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise customexception(e, sys)


"""        
if __name__ == "__main__":
    obj = PhobiaWordsCleaning()
    print(obj.preprocess_phobia_words("dark night full of darkness", "Achluophobia"))"""
