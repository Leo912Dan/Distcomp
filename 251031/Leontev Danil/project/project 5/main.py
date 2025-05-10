from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routers import router
from app.config import settings
from app.cache import cache

app = FastAPI(
    title="CRUD API for Writer, News, Label, Message",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorMessage": exc.detail,
            "errorCode": f"{exc.status_code:03d}01"
        }
    )

@app.on_event("startup")
async def startup_event():
    # Проверяем подключение к Redis
    try:
        cache.redis_client.ping()
        print("Successfully connected to Redis")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
    
    # Инициализация начальных данных
    from app.models import WriterRequestTo
    from app.services import WriterService
    try:
        WriterService.get_by_id(1)
    except HTTPException:
        WriterService.create(
            WriterRequestTo(
                login="example7@gmail.com",
                password="Turkey2727",
                firstname="Леонтьев",
                lastname="Данил"
            )
        )

@app.on_event("shutdown")
async def shutdown_event():
    # Очищаем кеш при завершении работы
    cache.clear()

app.include_router(router, prefix=settings.API_V1_STR)