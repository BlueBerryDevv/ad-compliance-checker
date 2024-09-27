from transformers import pipeline, AutoProcessor

class LLaVAModel:
    MODEL_ID = "llava-hf/llava-onevision-gemma2-7b-si-hf"

    def __init__(self):
        self.pipe = None
        self.processor = None

    def load_model(self):
        if self.pipe is None or self.processor is None:
            self.pipe = pipeline("image-to-text", model=self.MODEL_ID)
            self.processor = AutoProcessor.from_pretrained(self.MODEL_ID)
        return self.pipe, self.processor

# Global instance
llava_model = LLaVAModel().load_model()