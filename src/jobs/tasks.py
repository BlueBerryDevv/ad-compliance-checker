from rq import Queue
from redis import Redis
from collections import defaultdict
from models.ocr_model import perform_ocr
from models.yolo_model import process_image_yolo, classify_image, resize_and_pad
from models.gemma_model import check_repeat_punctuation

redis_conn = Redis()
q = Queue('ad_validation', connection=redis_conn)

def ocr_job(image_data):
    ocr_result = perform_ocr(image_data)
    # OCR 결과를 텍스트 분석 큐에 추가
    q.enqueue(text_analysis_job, ocr_result)
    return "OCR job completed and text analysis job queued"

def image_analysis_job(image_data, mode):
    # 기본값이 "Safe"인 defaultdict 생성
    result = defaultdict(lambda: "SAFE")
    
    if mode == "simple":
        sexual_result = classify_image(image_data)
        if sexual_result == 'nsfw':
            result['sexual'] = 'RISK'
        else:
            result['sexual'] = 'SAFE'
    elif mode == "detail":
        image_np = resize_and_pad(image_data)
        sexual_result = process_image_yolo(image_np)
        result['sexual'] = sexual_result
    else:
        return "Invalid mode"
    
    return {
        "Sexual Contents": result.get("RISK", "SAFE"),
        "Violent content": result.get("RISK", "SAFE"),
        "Unidentified images": result.get("unidentified", "RISK")
    }

def text_analysis_job(text_data):
    punc_status, punc_reason = check_repeat_punctuation(text_data)
    # analysis_result = analyze_text(text_data)
    
    analysis_result['contacts']
    return {
        "Misuse of ad features": analysis_result.get("misuse", "Caution"),
        "Contacts in ad text": analysis_result.get("contacts", "RISK"),
        "Business name requirements": analysis_result.get("business_name", "SAFE"),
        "Unidentified business": analysis_result.get("unidentified_business", "SAFE"),
        "Style and Spelling": analysis_result.get("style_spelling", "Caution"),
        "Dangerous products or services": analysis_result.get("dangerous_products", "SAFE")
    }