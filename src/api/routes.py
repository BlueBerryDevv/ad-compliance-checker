from fastapi import APIRouter, File, UploadFile, Form
from jobs.tasks import q, ocr_job, image_analysis_job, text_analysis_job

# PREFIX를 포함한 라우터 생성
router = APIRouter(prefix="/ad_compliance_checker")

@router.post("/ocr")
async def ocr_route(image: UploadFile = File(...)):
    image_data = await image.read()
    job = q.enqueue(ocr_job, image_data)
    return {"job_id": job.id}

@router.post("/image-analysis")
async def image_analysis_route(image: UploadFile = File(...), mode: str = Form(...)):
    image_data = await image.read()
    job = q.enqueue(image_analysis_job, image_data, mode)
    return {"job_id": job.id}

@router.post("/text-analysis")
async def text_analysis_route(text: str = Form(...)):
    job = q.enqueue(text_analysis_job, text)
    return {"job_id": job.id}

@router.get("/job-result/{job_id}")
async def get_job_result(job_id: str):
    job = q.fetch_job(job_id)
    if job is None:
        return {"status": "not found"}
    if job.is_finished:
        return {"status": "completed", "result": job.result}
    elif job.is_failed:
        return {"status": "failed", "error": str(job.exc_info)}
    else:
        return {"status": "pending"}