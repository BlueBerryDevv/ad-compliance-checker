from redis import Redis
from rq import Queue

redis_conn = Redis(host='localhost', port=6379, db=0)
q = Queue('ad_validation', connection=redis_conn)

def enqueue_job(job_function, *args, **kwargs):
    return q.enqueue(job_function, *args, **kwargs)

def get_job_result(job_id):
    job = q.fetch_job(job_id)
    if job is None:
        return None
    if job.is_finished:
        return job.result
    elif job.is_failed:
        return {"error": str(job.exc_info)}
    else:
        return {"status": "pending"}