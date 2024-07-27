from src.logger.logger import logger
from src.exceptions.exception import customexception
import pandas as pd
import mlflow
from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split
from PIL import Image
import os
from transformers import ViTFeatureExtractor
from torchvision.transforms import Compose, Resize, Normalize, ToTensor
from sklearn.preprocessing import LabelEncoder
from transformers import ViTForImageClassification, TrainingArguments, Trainer
from torchvision.transforms import Compose, Resize, Normalize, ToTensor, RandomHorizontalFlip, RandomRotation, ColorJitter, RandomResizedCrop, GaussianBlur
from datasets import load_metric
import numpy as np
import torch
import sys
from src.utils.utils import ModelSaveAndLoad

class ImageEmotionDetection:
    def __init__(self):
        self.model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224-in21k', num_labels=7)
        self.feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        self.normalize = Normalize(mean=self.feature_extractor.image_mean, std=self.feature_extractor.image_std)
        self.transform = Compose([
            RandomResizedCrop(self.feature_extractor.size["height"]),
            RandomHorizontalFlip(),
            RandomRotation(15),
            ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.3),
            GaussianBlur(3),
            ToTensor(),
            self.normalize
        ])
        self.label_encoder = LabelEncoder()
        self.ModelSaveAndLoad = ModelSaveAndLoad()
        self.accuracy_metric = load_metric("accuracy", trust_remote_code=True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    
    def load_data(self, data_dir, max_images_per_class=4000):
        try:
            labels = os.listdir(data_dir)
            data = []
            for label in labels:
                class_dir = os.path.join(data_dir, label)
                # Check if it's a directory before iterating
                if os.path.isdir(class_dir):
                    img_files = os.listdir(class_dir)[:max_images_per_class]  # Limit to max_images_per_class
                    for img_file in img_files:
                        img_path = os.path.join(class_dir, img_file)
                        data.append((img_path, label))
            return pd.DataFrame(data, columns=['image_path', 'label'])
        
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
    
    def df_to_dataset(self, df):
        return Dataset.from_pandas(df)
    
    def preprocess(self, examples):
        try:
            examples['pixel_values'] = [self.transform(Image.open(path).convert("RGB")) for path in examples['image_path']]
            examples['label'] = self.label_encoder.transform(examples['label'])
            return examples
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
    
    def compute_metrics(self, p):
        try:
            predictions, labels = p
            preds = np.argmax(predictions, axis=1)
            accuracy = self.accuracy_metric.compute(predictions=preds, references=labels)
            return {"accuracy": accuracy["accuracy"]}
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
    
    def preprocess_dataset(self):
        try:
            train_data_dir = "data/face-expression-recognition-dataset/images/images/train"
            val_data_dir = "data/face-expression-recognition-dataset/images/images/validation"
            
            logger.info(f"Loading training data from {train_data_dir}")
            train_data = self.load_data(train_data_dir)
            logger.info(f"Loaded {len(train_data)} training samples")

            logger.info(f"Loading validation data from {val_data_dir}")
            val_data = self.load_data(val_data_dir)
            logger.info(f"Loaded {len(val_data)} validation samples")
            
            train_dataset = self.df_to_dataset(train_data)
            val_dataset = self.df_to_dataset(val_data)
            
            all_labels = pd.concat([train_data['label'], val_data['label']]).unique()
            self.label_encoder.fit(all_labels)
            
            train_dataset = train_dataset.map(self.preprocess, batched=True, remove_columns=['image_path'])
            val_dataset = val_dataset.map(self.preprocess, batched=True, remove_columns=['image_path'])
            
            train_data['label'] = self.label_encoder.transform(train_data['label'])
            val_data['label'] = self.label_encoder.transform(val_data['label'])
            
            train_dataset.set_format(type='torch', columns=['pixel_values', 'label'])
            val_dataset.set_format(type='torch', columns=['pixel_values', 'label'])
            
            return train_dataset, val_dataset
        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)

    def detect_emotion(self, train_dataset, val_dataset):
        try:
            # Define training arguments
            training_args = TrainingArguments(
                output_dir='./results',
                eval_strategy="steps",
                per_device_train_batch_size=1,
                per_device_eval_batch_size=1,
                num_train_epochs=20,
                learning_rate=3e-5,
                weight_decay=0.01,
                save_total_limit=3,
                lr_scheduler_type='cosine',
                warmup_steps=500,
                logging_dir='./logs',
                logging_steps=10,
                metric_for_best_model='accuracy',
                load_best_model_at_end=True,
            )

            # Initialize Trainer
            trainer = Trainer(
                model=self.model.to(self.device),
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                tokenizer=self.feature_extractor,
                compute_metrics=self.compute_metrics,
            )

            # Start MLflow run
            with mlflow.start_run():
                mlflow.log_params(training_args.to_dict()) 
                mlflow.autolog()

                # Train the model
                trainer.train()

                # Evaluate the model
                eval_results = trainer.evaluate()
                print(f"Evaluation results: {eval_results}")

                # Log evaluation results
                mlflow.log_metrics(eval_results)

                # Save the model
                self.ModelSaveAndLoad.save_model(trainer, "artifacts/model/emotionclassification")

        except Exception as e:
            logger.info(customexception(e, sys))
            raise customexception(e, sys)
    