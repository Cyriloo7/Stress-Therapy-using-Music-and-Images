import sys
from src.logger.logger import logger
from src.exceptions.exception import customexception


class DivideInToFourParts:
    def __init__(self):
        pass

    def word_count(self, text):
        """
        Count the number of words in the given text.

        Parameters:
        text (str): The input text.

        Returns:
        int: The number of words in the text.
        """
        return len(text.split())

    def divide_into_four_parts(self, text, num_parts=4):
        """
        Divide the given text into parts based on the number of words.

        Parameters:
        text (str): The input text.
        num_parts (int, optional): The number of parts to divide the text into. Defaults to 4.

        Returns:
        list: A list of strings, where each string represents a part of the divided text.

        Raises:
        customexception: If an exception occurs during the division process.
        """
        try:
            word_count = self.word_count(text)
            num_parts = min(
                6, (word_count - 1) // 15 + 1
            )  # Calculate number of parts based on word count
            logger.info("divide_text_into_parts started")
            sentences = text.split(". ")
            sentences_per_part = -(
                -len(sentences) // num_parts
            )  # Calculate sentences per part
            divided_parts = [
                ". ".join(
                    sentences[i * sentences_per_part : (i + 1) * sentences_per_part]
                )
                for i in range(num_parts)
            ]
            logger.info("divide_text_into_parts finished")
            return divided_parts
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)


"""if __name__ == "__main__":
    text = "Goin' out tonight, changes into something red. Her mother doesn't like that kind of dress. She's headin' for something that she won't forget. She doesn't even know that she's fallin'. We're only gettin' older, baby. The night changes very fast. Disappearing when you wake up is nothing to be afraid of. Even though the night changes, it will never change me and you. The thought brings her back to the memories of the lost piece of innocence that she lost. The thoughts are brought back to her by the moonlight. It is impossible for the night to change, but it is possible for the people with whom I am with.    - The song by The Beatles.Goin' out tonight, changes into something red. Her mother doesn't like that kind of dress. She's headin' for something that she won't forget. She doesn't even know that she's fallin'. We're only gettin' older, baby. The night changes very fast. Disappearing when you wake up is nothing to be afraid of. Even though the night changes, it will never change me and you. The thought brings her back to the memories of the lost piece of innocence that she lost. The thoughts are brought back to her by the moonlight. It is impossible for the night to change, but it is possible for the people with whom I am with.    - The song by The Beatles"
    div_obj = DivideInToFourParts()
    divided_parts = div_obj.divide_into_four_parts(text)
    for i, part in enumerate(divided_parts, start=1):
        print(f"Part {i}: {part}")
"""
