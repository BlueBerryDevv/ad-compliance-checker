import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import torch
from models.common import DetectMultiBackend, NSFWModel
from utils.general import (check_img_size, non_max_suppression, scale_boxes, select_device)
from utils.plots import Annotator, colors


# Load classification model
nsfw_model = NSFWModel()
device = select_device('')
yolo_model = DetectMultiBackend('./weights/nsfw_detector_e_rok.pt', device=device, dnn=False, data=None, fp16=False)
stride, names, pt = yolo_model.stride, yolo_model.names, yolo_model.pt
imgsz = check_img_size((640, 640), s=stride)


def classify_image(input_image, conf_threshold=0.3, iou_threshold=0.45, label_mode="Draw box"):
    if isinstance(input_image, str):  # URL input
        response = requests.get(input_image)
        image = Image.open(BytesIO(response.content))
    else:  # File upload
        image = Image.fromarray(input_image)
    
    image_np = np.array(image)
    if len(image_np.shape) == 2:  # grayscale
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    elif image_np.shape[2] == 4:  # RGBA
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

    result = nsfw_model.predict(image)
    return result

def resize_and_pad(image, target_size= imgsz):
    ih, iw = image.shape[:2]
    target_h, target_w = target_size

    # 이미지의 가로세로 비율 계산
    scale = min(target_h/ih, target_w/iw)
    
    # 새로운 크기 계산
    new_h, new_w = int(ih * scale), int(iw * scale)
    
    # 이미지 리사이즈
    resized = cv2.resize(image, (new_w, new_h))
    
    # 패딩 계산
    pad_h = (target_h - new_h) // 2
    pad_w = (target_w - new_w) // 2
    
    # 패딩 추가
    padded = cv2.copyMakeBorder(resized, pad_h, target_h-new_h-pad_h, pad_w, target_w-new_w-pad_w, cv2.BORDER_CONSTANT, value=[0,0,0])
    
    return padded

def process_image_yolo(image, conf_threshold, iou_threshold, label_mode):
    # Image preprocessing
    im = torch.from_numpy(image).to(device).permute(2, 0, 1)
    im = im.half() if yolo_model.fp16 else im.float()
    im /= 255
    if len(im.shape) == 3:
        im = im[None]
    
    # Resize image
    im = torch.nn.functional.interpolate(im, size=imgsz, mode='bilinear', align_corners=False)
    
    # Inference
    pred = yolo_model(im, augment=False, visualize=False)
    if isinstance(pred, list):
        pred = pred[0]
        
    # NMS
    pred = non_max_suppression(pred, conf_threshold, iou_threshold, None, False, max_det=1000)
    # Process results
    detected_classes = set()
    
    for i, det in enumerate(pred):
        if len(det):
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], image.shape).round()
            
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)
                if c != 6:  # Ignore class 6
                    detected_classes.add(c)

    # Determine result based on detected classes
    if 4 in detected_classes and 10 in detected_classes:
        return "Approved_limited"
    elif detected_classes - {4, 6, 10}:  # If there are any classes other than 4, 6, and 10
        return "Risk"
    else:
        return "Safe"

def detect_objects(image):
    return ''