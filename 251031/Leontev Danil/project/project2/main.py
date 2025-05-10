from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routers import router

app = FastAPI(title="CRUD API for User, Topic, Mark, Message")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print(f"Exception handler called with status code {exc.status_code} and detail {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorMessage": exc.detail,
            "errorCode": f"{exc.status_code:03d}01"
        }
    )

@app.on_event("startup")
def seed_data():
    from app.models import UserRequestTo
    from app.services import UserService
    try:
        UserService.get_by_id(1)
    except HTTPException:
        UserService.create(
            UserRequestTo(
                login="awsduhjk@gmail.com",
                password="Turkey2727",
                firstname="Данил",
                lastname="Леонтьев"
            )
        )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=24110, reload=True)