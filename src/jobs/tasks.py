from rq import Queue
from redis import Redis
from collections import defaultdict
from models.ocr_model import perform_ocr
from models.yolo_model import classify_image, resize_and_pad
from models.llava_model import analyze_images_llava
from validators.text_validator import text_validate
from validators.drug_validator import check_drug
from models.ocr_model import Llava

redis_conn = Redis()
q = Queue('ad_validation', connection=redis_conn)

llava = Llava()

def ocr_job(image_data):
    ocr_result = llava.ask(image_data)
    # OCR 결과를 텍스트 분석 큐에 추가
    q.enqueue(text_analysis_job, ocr_result)
    return "OCR job completed and text analysis job queued"

def image_analysis_job(image_data, mode):
    # 기본값이 "Safe"인 defaultdict 생성
    result = defaultdict(lambda: "Safe")
    
    if mode == "simple":
        simple_result = classify_image(image_data)
        if simple_result == 'nsfw':
            result['Sexual Contents'] = 'Risk'
        else:
            result['Sexual Contents'] = 'Safe'
    elif mode == "detail":
        detail_result = analyze_images_llava(image_data)
    else:
        return "Invalid mode"
    
    return detail_result

def text_analysis_job(text_data):
    text_result = text_validate(text_data)
    drug_result = check_drug(text_data)
    text_result['prescription drugs'] = drug_result
    
    return text_result