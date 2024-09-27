from redis import Redis
from rq import Queue
from functools import lru_cache

@lru_cache()
def get_redis_connection():
    return Redis(host='localhost', port=6379, db=0)

@lru_cache()
def get_task_queue():
    redis_conn = get_redis_connection()
    return Queue('ad_validation', connection=redis_conn)