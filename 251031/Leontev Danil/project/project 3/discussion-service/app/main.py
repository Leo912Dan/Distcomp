from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .init_cassandra import wait_for_cassandra
from .router import router

app = FastAPI(title="Discussion Service", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация Cassandra
@app.on_event("startup")
async def startup_event():
    wait_for_cassandra()

# Подключаем роутер
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 