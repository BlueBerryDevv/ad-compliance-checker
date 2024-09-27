from fastapi import FastAPI
from api.routes import router as ad_compliance_router
from api.dependencies import get_redis_connection, get_task_queue

app = FastAPI(title="Ad Inspector API")

@app.on_event("startup")
async def startup_event():
    # 애플리케이션 시작 시 필요한 초기화 작업을 수행합니다.
    app.state.redis = get_redis_connection()
    app.state.task_queue = get_task_queue()

@app.on_event("shutdown")
async def shutdown_event():
    # 애플리케이션 종료 시 필요한 정리 작업을 수행합니다.
    app.state.redis.close()

# 라우터 등록
app.include_router(ad_compliance_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Ad Compliance Checker API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)