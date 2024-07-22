from src.logger.logger import logger
import sys
from src.exceptions.exception import customexception
from src.components.text_summarization import TextSummarizer
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import requests
import torch
import io

class TextToImage:
    def __init__(self):
        self.API_TOKEN = "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"
        self.API_URL = "https://api-inference.huggingface.co/models/fluently/Fluently-XL-Final"
        self.headers = {"Authorization": f"Bearer {self.API_TOKEN}"}

        self.summarizer = TextSummarizer()

        self.nsfw_processor = AutoImageProcessor.from_pretrained("giacomoarienti/nsfw-classifier")
        self.nsfw_model = AutoModelForImageClassification.from_pretrained("giacomoarienti/nsfw-classifier")

        torch.cuda.empty_cache()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.negative_prompts = ["pornography", "bed", "cot", "matress", "sleep", "pillow", "bondage", "breast", "sofa", "cleavage", "sexy", "seductive", "ass", "porn", "(((deformed)))", "blurry", "bad anatomy",
                                 "disfigured", "poorly drawn face", "mutation", "mutated", "(extra_limb)", "(ugly)", "censored", "censor_bar", "multiple breasts", "(mutated hands and fingers:1.5)",
                                 "(long body :1.3)", "(mutation, poorly drawn :1.2)", "black-white", "bad anatomy", "liquid body", "liquid tongue", "disfigured", "malformed", "mutated", "anatomical nonsense",
                                 "text font ui", "error", "malformed hands", "long neck", "blurred", "lowers", "low res", "bad proportions", "bad shadow", "uncoordinated body", "unnatural body", "fused breasts",
                                 "bad breasts", "huge breasts", "poorly drawn breasts", "extra breasts", "liquid breasts", "heavy breasts", "missing breasts", "huge haunch", "huge thighs", "huge calf", "bad hands",
                                 "fused hand", "missing hand", "disappearing arms", "disappearing thigh", "disappearing calf", "disappearing legs", "fused ears", "bad ears", "poorly drawn ears",
                                 "extra ears", "liquid ears", "heavy ears", "missing ears", "old photo", "black and white filter", "colorless", "(((deformed)))", "blurry", "bad anatomy",
                                 "disfigured", "poorly drawn face", "mutation", "mutated", "(extra_limb)", "(ugly)", "(poorly drawn hands)", "fused fingers", "messy drawing", "broken legs", "censor",
                                 "censored", "censor_bar", "multiple breasts", "(mutated hands and fingers:1.5)", "(long body :1.3)", "(mutation, poorly drawn :1.2)", "black-white", "bad anatomy",
                                 "liquid body", "liquid tongue", "disfigured", "malformed", "mutated", "anatomical nonsense", "text font ui", "error", "malformed hands", "long neck", "blurred", "lowers", "low res",
                                 "bad proportions", "bad shadow", "uncoordinated body", "unnatural body", "fused breasts", "bad breasts", "huge breasts", "poorly drawn breasts", "extra breasts", "liquid breasts",
                                 "heavy breasts", "missing breasts", "huge haunch", "huge thighs", "huge calf", "bad hands", "fused hand", "missing hand", "disappearing arms", "disappearing thigh",
                                 "disappearing calf", "disappearing legs", "fused ears", "bad ears", "poorly drawn ears", "extra ears", "liquid ears", "heavy ears", "missing ears", "NSFW", "Naked", "Nude"]

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.content

    def text_to_image(self, lt):
        for i, inp in enumerate(lt):
            j = 0
            try:
                progress = True
                while progress:
                    logger.info("Image generation API call initiated")
                    image_bytes = self.query({"inputs": ("beautiful image of : " + inp), "negative_prompt": self.negative_prompts})
                    image = Image.open(io.BytesIO(image_bytes))
                    # Resize the image to the desired dimensions
                    desired_width = 900
                    desired_height = 600
                    image = image.resize((desired_width, desired_height), Image.LANCZOS)
                    logger.info("Image is resized")

                    if image:
                        with torch.no_grad():
                            inputs = self.nsfw_processor(images=image, return_tensors="pt")
                            outputs = self.nsfw_model(**inputs)
                            logits = outputs.logits

                        predicted_label = logits.argmax(-1).item()
                        image_type = self.nsfw_model.config.id2label[predicted_label]
                        logger.info(f"Generated image {i + 1} is {image_type} image.")
                        print(image_type)

                        if image_type == "neutral" or image_type == "drawings":
                            j = 0
                            image.save(f'artifacts/Generated image/Generated_image{i}.jpg', 'JPEG')
                            progress = False
                        else:
                            logger.info(f"Generated image {i + 1} is {image_type} image. Retrying...")
                            print(f"Generated image {i + 1} is {image_type} image. Retrying...")
                            inp = self.summarizer.third_summarize(inp)
                            inp = "scenery image of, " + inp
                            j += 1

                            if j == 3:
                                progress = False
                    torch.cuda.empty_cache()
                    logger.info(f"{i} Image generation API call completed")

            except Exception as e:
                print(f"Error generating image {i + 1}: {str(e)}")
                logger.error(f"Error generating image {i + 1}: {str(e)}")


"""if __name__ == "__main__":
    obj = TextToImage()
    input_txt = ["a cat", "a dog", "a tiger", "an elephant"]
    obj.text_to_image(input_txt)"""
