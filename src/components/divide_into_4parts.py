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
        

"""if __name__ == '__main__':
    text = "Goin' out tonight, changes into something red Her mother doesn't like that kind of dress Everything she never had she's showin' off Drivin' too fast, moon is breakin' through her hair She's headin' for somethin' that she won't forget Havin' no regrets is all that she really wants We're only gettin' older, baby And I've been thinkin' about it lately Does it ever drive you crazy Just how fast the night changes? Everything that you've ever dreamed of Disappearing when you wake up But there's nothing to be afraid of Even when the night changes It will never change me and you Chasing it tonight, doubts are runnin' 'round her head He's waitin', hides behind a cigarette Heart is beatin' loud and she doesn't want it to stop Movin' too fast, moon is lightin' up her skin She's fallin', doesn't even know it yet Havin' no regrets is all that she really wants We're only gettin' older, baby And I've been thinkin' about it lately Does it ever drive you crazy Just how fast the night changes? Everything that you've ever dreamed of Disappearing when you wake up But there's nothing to be afraid of Even when the night changes It will never change me and you Goin' out tonight, changes into something red Her mother doesn't like that kind of dress Reminds her of the missin' piece of innocence she lost We're only gettin' older, baby And I've been thinkin' about it lately Does it ever drive you crazy Just how fast the night changes? Everything that you've ever dreamed of Disappearing when you wake up But there's nothing to be afraid of Even when the night changes It will never change, baby It will never change, baby It will never change me and you"
    div_obj = DivideInToFourParts()
    divided_parts = div_obj.divide_into_four_parts(text)
    for i, part in enumerate(divided_parts, start=1):
        print(f"Part {i}: {part}")"""