from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "running"}

@app.get("/upload")
async def upload(url: str):

    print(f"Download URL: {url}")

    return JSONResponse({
        "status": "ok",
        "url": url
    })