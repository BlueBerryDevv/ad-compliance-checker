from transformers import AutoModelForImageClassification, ViTImageProcessor
import torch
from PIL import Image

class NSFWModel:
    def __init__(self):
        self.model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        self.processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')
        self.id2label = self.model.config.id2label

    def predict(self, image: Image.Image) -> str:
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_label = logits.argmax(-1).item()
            
            return self.id2label[predicted_label]