from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routers import router

# Создаем экземпляр FastAPI приложения
# title используется для автоматической генерации документации
app = FastAPI(title="CRUD API for User, Topic, Mark, Message")

# Глобальный обработчик HTTP исключений
# Преобразует все HTTPException в JSON-ответ с единым форматом
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print(f"Exception handler called with status code {exc.status_code} and detail {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorMessage": exc.detail,
            "errorCode": f"{exc.status_code:03d}01"  # Формат кода ошибки: XXX01
        }
    )

# Функция, выполняемая при запуске приложения
# Создает тестового пользователя, если база пуста
@app.on_event("startup")
def seed_data():
    from app.models import UserRequestTo
    from app.services import UserService
    try:
        # Проверяем, существует ли пользователь с ID 1
        UserService.get_by_id(1)
    except HTTPException:
        # Если нет - создаем тестового пользователя
        UserService.create(
            UserRequestTo(
                login="awsduhjk@gmail.com",
                password="Turkey2727",
                firstname="Данил",
                lastname="Леонтьев"
            )
        )

# Подключаем роутер с префиксом /api/v1.0
app.include_router(router)

# Точка входа для запуска приложения
if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на всех интерфейсах (0.0.0.0) порт 24110
    # reload=True включает автоматическую перезагрузку при изменении кода
    uvicorn.run("main:app", host="0.0.0.0", port=24110, reload=True)