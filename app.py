from fastapi import FastAPI
import aiohttp
import os

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/upload")
async def upload(url: str):

    filename = url.split("/")[-1]

    if not filename:
        filename = "download.file"

    filepath = f"/tmp/{filename}"

    print("Downloading:", url)
    print("Saving to:", filepath)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            if response.status != 200:
                return {
                    "status": "error",
                    "code": response.status
                }

            with open(filepath, "wb") as f:
                while True:
                    chunk = await response.content.read(1024 * 1024)

                    if not chunk:
                        break

                    f.write(chunk)

    size = os.path.getsize(filepath)

    print("Download finished")
    print("File size:", size)

    return {
        "status": "downloaded",
        "filename": filename,
        "size": size,
        "path": filepath
    }