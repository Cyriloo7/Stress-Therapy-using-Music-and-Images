from src.exceptions.exception import customexception
from src.logger.logger import logger
import sys
import os
from transformers import ViTForImageClassification

class ModelSaveAndLoad:
    def __init__(self):
        pass

    def save_model(self, model, file_path):
        try:
            dir_path = os.path.dirname(file_path)

            os.makedirs(dir_path, exist_ok=True)
            model.save_pretrained(file_path)
        
        except Exception as e:
            raise customexception(e, sys)
            

    def load_model(self):
        try:
            return ViTForImageClassification.from_pretrained('artifacts/model/emotionclassification')
        
        except Exception as e:
            raise customexception(e, sys)