from src.logger.logger import logger
import sys
from src.exceptions.exception import customexception
import pickle
import json


class StressDetection:
    def __init__(self):
        #logger.info("StressDetection Model loading...")
        try:
            with open('artifacts/model/detection_new.pkl', 'rb') as f:
                self.detection_model = pickle.load(f)
            #logger.info("StressDetection Model loaded successfully.")
        except Exception as e:
            raise customexception(e, sys)
    
    
    def get_input_feature_json_file(self, json_file):

        try:
            #logger.info("Reading json file...")
            with open(json_file, "r") as read_content: 
                data = json.load(read_content)
            #logger.info("Extracting features from json file...")
            features = [
                data.get('MEAN_RR'),
                data.get('MEDIAN_RR'),
                data.get('SDRR'),
                data.get('RMSSD'),
                data.get('SDSD'),
                data.get('SDRR_RMSSD'),
                data.get('HR'),
                data.get('pNN25'),
                data.get('pNN50'),
                data.get('SD1'),
                data.get('SD2'),
                data.get('KURT'),
                data.get('SKEW'),
                data.get('MEAN_REL_RR'),
                data.get('MEDIAN_REL_RR'),
                data.get('SDRR_REL_RR'),
                data.get('RMSSD_REL_RR'),
                data.get('SDSD_REL_RR'),
                data.get('SDRR_RMSSD_REL_RR'),
                data.get('KURT_REL_RR'),
                data.get('SKEW_REL_RR'),
                data.get('VLF'),
                data.get('VLF_PCT'),
                data.get('LF'),
                data.get('LF_PCT'),
                data.get('LF_NU'),
                data.get('HF'),
                data.get('HF_PCT'),
                data.get('HF_NU'),
                data.get('TP'),
                data.get('LF_HF'),
                data.get('HF_LF'),
                data.get('sampen'),
                data.get('higuchi')
            ]
            #logger.info("Features extracted successfully")
            return features
        except Exception as e:
            raise customexception(e, sys)
    
    def detect_stress(self, json_data):

        try:
            #logger.info("Detecting stress level...")
            features = self.get_input_feature_json_file(json_data)
            detection_prediction = self.detection_model.predict([features])
            #logger.info("Stress level detected")
            return detection_prediction
        except Exception as e:
            raise customexception(e, sys)
    

#if __name__=="__main__":
#    obj = StressDetection()
#    print(obj.detect_stress(r"C:\Users\cyril\Downloads\flask inout json\flask inout json\no_stress_1.json"))