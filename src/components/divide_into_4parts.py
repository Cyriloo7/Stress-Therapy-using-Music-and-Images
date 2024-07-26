import sys
from src.logger.logger import logger
from src.exceptions.exception import customexception

class DivideInToFourParts:
    def __init__(self):
        pass

    def divide_into_four_parts(self, text, num_parts=4):
        try:
            logger.info("divide_text_into_parts started")
            # Split the text into sentences based on full stops
            sentences = text.split('. ')

            # Calculate the number of sentences per part
            sentences_per_part = len(sentences) // num_parts
            print(sentences_per_part)

            # Initialize an empty list to store the divided parts
            divided_parts = []

            # Loop through the sentences and create parts
            for i in range(num_parts):
                start_index = i * sentences_per_part
                end_index = (i + 1) * sentences_per_part if i < num_parts - 1 else len(sentences)
                part = '. '.join(sentences[start_index:end_index])
                divided_parts.append(part)
            logger.info("divide_text_into_parts finished")
            return divided_parts
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)