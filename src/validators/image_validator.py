import requests
from PIL import Image
from typing import List, Union, Dict

from models.llava_model import llava_model
from utils.prompts import image_inst_system_message

def analyze_images(images: Union[str, List[str], Image.Image, List[Image.Image]]) -> List[Dict[str, str]]:
    pipe, processor = llava_model

    if isinstance(images, (str, Image.Image)):
        images = [images]

    processed_images = []
    for img in images:
        if isinstance(img, str):
            if img.startswith('http'):
                img = Image.open(requests.get(img, stream=True).raw)
            else:
                img = Image.open(img)
        processed_images.append(img)

    image_count = len(processed_images)
    s_str_bool = 's' if image_count > 1 else ''
    system_message = image_inst_system_message(image_count, s_str_bool)

    results = []
    for i, img in enumerate(processed_images, start=1):
        conversation = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_message}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analyze image {i}:"},
                    {"type": "image"},
                ],
            },
        ]
        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        output = pipe(img, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
        
        # Extract the classifications from the generated text
        generated_text = output[0]['generated_text']
        classifications = {}
        for line in generated_text.split('\n'):
            if ':' in line:
                category, classification = line.split(':')
                classification = classification.strip()
                if classification not in ['Safe', 'Risk', 'approved_rimit']:
                    classification = 'Risk'  # Default to Risk if the output is unexpected
                classifications[category.strip()] = classification
        
        results.append(classifications)

    return results