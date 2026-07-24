from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from downloader import download_file
from logger import logger
from config import APP_NAME, APP_VERSION
from files import list_files


# ----------------------------------
# Lifespan
# ----------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 50)
    logger.info(f"{APP_NAME} v{APP_VERSION} started")
    logger.info("=" * 50)

    yield

    logger.info("=" * 50)
    logger.info("Application stopped")
    logger.info("=" * 50)


app = FastAPI(

    title=APP_NAME,

    version=APP_VERSION,

    lifespan=lifespan

)


# ----------------------------------
# Request Logger Middleware
# ----------------------------------

@app.middleware("http")
async def request_logger(request: Request, call_next):

    start = time.time()

    client = request.client.host if request.client else "unknown"

    logger.info(
        f"{client} -> {request.method} {request.url.path}"
    )

    try:

        response = await call_next(request)

    except Exception:

        logger.exception("Unhandled Exception")

        raise

    elapsed = round(time.time() - start, 3)

    logger.info(

        f"{request.method} "

        f"{request.url.path} "

        f"{response.status_code} "

        f"{elapsed}s"

    )

    return response


# ----------------------------------
# Root
# ----------------------------------

@app.get("/")

async def root():

    return {

        "service": APP_NAME,

        "version": APP_VERSION,

        "status": "running"

    }


# ----------------------------------
# Health Check
# ----------------------------------

@app.get("/health")

async def health():

    return {

        "status": "ok"

    }


# ----------------------------------
# Download Endpoint
# ----------------------------------

@app.get("/upload")

async def upload(url: str):

    result = await download_file(url)

    return result

# ----------------------------------
# List Files
# ----------------------------------

@app.get("/files")

async def files():

    return list_files()

# ----------------------------------
# HTTP Exception
# ----------------------------------

@app.exception_handler(HTTPException)

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):

    logger.warning(

        f"HTTP {exc.status_code} | {exc.detail}"

    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "status": "error",

            "code": exc.status_code,

            "message": exc.detail,

        },

    )


# ----------------------------------
# Global Exception
# ----------------------------------

@app.exception_handler(Exception)

async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    logger.exception(str(exc))

    return JSONResponse(

        status_code=500,

        content={

            "status": "error",

            "code": 500,

            "message": "Internal Server Error",

        },

    )