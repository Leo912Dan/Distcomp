from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routers import router
from app.services.kafka_service import kafka_service

app = FastAPI(title="CRUD API for User, Topic, Mark, Message")

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
    from app.models import UserRequestTo
    from app.services import UserService
    try:
        UserService.get_by_id(1)
    except HTTPException:
        UserService.create(
            UserRequestTo(
                login="sagatovmirsaid7@gmail.com",
                password="Turkey2727",
                firstname="Мирсаид",
                lastname="Сагатов"
            )
        )
    
    # Инициализация Kafka
    await kafka_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_service.stop()

app.include_router(router)