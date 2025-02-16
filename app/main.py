import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.routes.matches import matches_router
from app.routes.tournaments import tournaments_router
from app.routes.users import users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tournaments_router)
app.include_router(matches_router)
app.include_router(users_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    custom_errors = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        msg = f"'{field}' is required but missing!" if error["type"] == "value_error.missing" else error["msg"]
        custom_errors.append({"field": field, "error": msg})

    return JSONResponse(
        status_code=422,
        content={"detail": custom_errors},
    )


if __name__ == "__main__":
    uvicorn.run(app)
