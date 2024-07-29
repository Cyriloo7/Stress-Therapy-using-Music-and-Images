from transformers import pipeline
import torch
import sys
from src.logger.logger import logger
from src.exceptions.exception import customexception
import mlflow
import boto3
from botocore.exceptions import ClientError
import json
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Text models"

    def __init__(self, message):
        self.message = message



class TextSummarizer:
    def __init__(self):
        logger.info("TextSummarizer model initialized")
        self.pipe = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

    def generate_text(self, model_id, body):

        logger.info(
            "Generating text with Amazon Titan Text model %s", model_id)

        bedrock = boto3.client(service_name='bedrock-runtime')

        accept = "application/json"
        content_type = "application/json"

        response = bedrock.invoke_model(
            body=body, modelId=model_id, accept=accept, contentType=content_type
        )

        response_body = json.loads(response.get("body").read())

        finish_reason = response_body.get("error")

        if finish_reason is not None:
            raise ImageError(f"Text generation error. Error is {finish_reason}")

        logger.info(
            "Successfully generated text with Amazon Titan Text model %s", model_id)

        return response_body

    def first_summarize(self, text):
        model_id = 'amazon.titan-text-express-v1'
        try:
            logger.info("first summarization started")
            if isinstance(text, bytes):
                  text = text.decode('utf-8')
            max_input_length = 42000
            if len(text) > max_input_length:
                logger.info("Input text is too long, truncating.")
                text = text[:max_input_length]
            input_text = f""" <<SYS>>
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

        <</SYS>>
            Here are the lyrics to a song. Please provide a brief summary of the lyrics.

                        Lyrics:

                        {text}

                        Summary: """
            
            body = json.dumps({
                "inputText": str(input_text),
                "textGenerationConfig": {
                    "maxTokenCount": 3072,
                    "stopSequences": [],
                    "temperature": 0.5,
                    "topP": 0.9
                }
            })

            max_retries = 3
            retries = 0
            summary = None

            while retries < max_retries:
                response_body = self.generate_text(model_id, body)
                for result in response_body['results']:
                    summary = result['outputText']
                if summary and "unable to respond to the prompt" not in summary:
                    break
                retries += 1
                time.sleep(2)
            logger.info(f"summary: {summary}")
            logger.info("first summarization finished")
            return summary
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
          

    def second_summarize(self, text):
          try:
               logger.info("second summarization started")
               if isinstance(text, bytes):
                  text = text.decode('utf-8')
               with torch.no_grad():
                   torch.cuda.empty_cache()
                   summary = self.pipe(str(text),max_length=200, min_length=30, do_sample=True, clean_up_tokenization_spaces=True)
               logger.info(" second summarization finished")
               return summary[0]['summary_text']
          except Exception as e:
               logger.info(customexception(e, sys))
               raise customexception(e, sys)
          
    def third_summarize(self, text):
        """try:
               logger.info("second summarization started")
               if isinstance(text, bytes):
                  text = text.decode('utf-8')
               with torch.no_grad():
                   torch.cuda.empty_cache()
                   summary = self.pipe(str(text),max_length=200, min_length=10, do_sample=True, clean_up_tokenization_spaces=True)
               logger.info(" second summarization finished")
               return summary[0]['summary_text']
          except Exception as e:
               logger.info(customexception(e, sys))
               raise customexception(e, sys)"""
          
        model_id = 'amazon.titan-text-express-v1'
        try:
            logger.info("first summarization started")
            if isinstance(text, bytes):
                  text = text.decode('utf-8')
            max_input_length = 42000
            if len(text) > max_input_length:
                logger.info("Input text is too long, truncating.")
                text = text[:max_input_length]
            input_text = f""" <<SYS>>
                        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous,loneliness, sadness, isolation, struggling with emotions, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

                        <</SYS>>
                            Please provide a short summary of the lyrics by changing the context.

                        Lyrics:

                        {text}

                        Summary: """
            
            body = json.dumps({
                "inputText": str(input_text),
                "textGenerationConfig": {
                    "maxTokenCount": 2048,
                    "stopSequences": [],
                    "temperature": 0.5,
                    "topP": 0.9
                }
            })

            max_retries = 3
            retries = 0
            summary = None

            while retries < max_retries:
                response_body = self.generate_text(model_id, body)
                for result in response_body['results']:
                    summary = result['outputText']
                if summary and "unable to respond to the prompt" not in summary:
                    break
                retries += 1
                time.sleep(2)
            logger.info(f"summary: {summary}")
            logger.info("first summarization finished")
            return summary
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
          
          
"""      
if __name__ == "__main__":
     summarizer = TextSummarizer()
     print(summarizer.first_summarize("The club isn't the best place to find a lover So the bar is where I go Me and my friends at the table doing shots Drinking fast and then we talk slow Come over and start up a conversation with just me And trust me, I'll give it a chance Now take my hand, stop, put Van The Man on the jukebox And then we start to dance And now I'm singing like Girl, you know I want your love Your love was handmade for somebody like me Come on now, follow my lead I may be crazy, don't mind me Say: Boy, let's not talk too much Grab on my waist and put that body on me Come on now, follow my lead Come, come on now, follow my lead I'm in love with the shape of you We push and pull like a magnet do Although my heart is falling too I'm in love with your body And last night you were in my room And now my bedsheets smell like you Everyday discovering something brand new I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Everyday discovering something brand new I'm in love with the shape of you One week in, we let the story begin We're going out on our first date You and me are thrifty, so go all you can eat Fill up your bag and I fill up a plate We talk for hours and hours about the sweet and the sour And how your family is doing okay Leave and get in a taxi, then kiss in the backseat Tell the driver: Make the radio play And I'm singing like Girl, you know I want your love  Your love was handmade for somebody like me Come on now, follow my lead I may be crazy, don't mind me Say: Boy, let's not talk too much Grab on my waist and put that body on me Come on now, follow my lead Come, come on now, follow my lead I'm in love with the shape of you We push and pull like a magnet do Although my heart is falling too I'm in love with your body And last night you were in my room And now my bedsheets smell like you Everyday discovering something brand new I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Oh I, oh I, oh I, oh I I'm in love with your body Everyday discovering something brand new I'm in love with the shape of you Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on Come on, be my baby, come on I'm in love with the shape of you We push and pull like a magnet do Although my heart is falling too I'm in love with your body Last night you were in my room And now my bedsheets smell like you Everyday discovering something brand new I'm in love with your body Come on, be my baby, come on Come on, be my baby, come on (I'm in love with your body) Come on, be my baby, come on Come on, be my baby, come on (I'm in love with your body) Come on, be my baby, come on Come on, be my baby, come on (I'm in love with your body) Everyday discovering something brand new I'm in love with the shape of you"))
     print(summarizer.second_summarize("This is a sample text to summarize."))"""
