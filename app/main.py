from fastapi import FastAPI,Request,HTTPException
from app.routes import routes,auth
from app.data.connection import init_db
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger

init_db()

app=FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )

app.include_router(routes.router)
app.include_router(auth.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    errors = []
    logger.error("Invalid JWT token")
    for err in exc.errors():
        errors.append({
            "field": err["loc"][-1],
            "message": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception("Unexpected server error")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )

@app.middleware("http")
async def log_requests(request, call_next):

    logger.info(f"{request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response