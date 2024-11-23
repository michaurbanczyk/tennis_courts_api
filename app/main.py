from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"response": "API is working!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
