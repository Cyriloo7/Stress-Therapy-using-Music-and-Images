from src.logger.logger import logger
from src.exceptions.exception import customexception
from src.components.model_trainer import ImageEmotionDetection
import sys

ImageEmotionDetection = ImageEmotionDetection()

try:
    train_dataset, val_dataset = ImageEmotionDetection.preprocess_dataset()
    ImageEmotionDetection.detect_emotion(train_dataset, val_dataset)

except Exception as e:
    raise customexception(e, sys)