from transformers import pipeline
import torch
import sys
from src.logger.logger import logger
from src.exceptions.exception import customexception

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TextSummarizer:
     def __init__(self):
          logger.info("TextSummarizer model initialized")
          self.pipe = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

     def first_summarize(self, text):
        try:
            logger.info("first summarization started")
            if isinstance(text, bytes):
                  text = text.decode('utf-8')
            with torch.no_grad():
                torch.cuda.empty_cache()
                summary = self.pipe(str("summary of : " + text), max_length=512, min_length=150, do_sample=True, clean_up_tokenization_spaces=True)
            logger.info("first summarization finished")
            summary = summary[0]['summary_text']
            return summary
        except Exception as e:
            raise customexception(e, sys)
          

     def second_summarize(self, text):
          try:
               logger.info("second summarization started")
               if isinstance(text, bytes):
                  text = text.decode('utf-8')
               with torch.no_grad():
                   torch.cuda.empty_cache()
                   summary = self.pipe(str("summary of : "+text),max_length=200, min_length=30, do_sample=True, clean_up_tokenization_spaces=True)
               logger.info(" second summarization finished")
               return summary[0]['summary_text']
          except Exception as e:
               raise customexception(e, sys)
          
     def third_summarize(self, text):
          try:
               logger.info("second summarization started")
               if isinstance(text, bytes):
                  text = text.decode('utf-8')
               with torch.no_grad():
                   torch.cuda.empty_cache()
                   summary = self.pipe(str("summary of : "+text),max_length=200, min_length=20, do_sample=True, clean_up_tokenization_spaces=True)
               logger.info(" second summarization finished")
               return summary[0]['summary_text']
          except Exception as e:
               raise customexception(e, sys)
          
"""if __name__ == "__main__":
     summarizer = TextSummarizer()
     print(summarizer.first_summarize("This is a sample text to summarize."))
     print(summarizer.second_summarize("This is a sample text to summarize."))"""
