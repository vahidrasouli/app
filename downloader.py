import asyncio
import os
import time

import aiohttp
from fastapi import HTTPException

from config import (
    CHUNK_SIZE,
    CONNECT_TIMEOUT,
    DEFAULT_HEADERS,
    DOWNLOAD_DIR,
    MAX_FILE_SIZE,
    MAX_REDIRECTS,
    SOCK_READ_TIMEOUT,
    TOTAL_TIMEOUT,
)

from logger import logger
from security import (
    generate_safe_filename,
    validate_download_url,
)


async def download_file(url: str):

    # ----------------------------
    # Validate URL
    # ----------------------------

    validate_download_url(url)

    filename = generate_safe_filename(url)

    filepath = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    timeout = aiohttp.ClientTimeout(

        total=TOTAL_TIMEOUT,

        connect=CONNECT_TIMEOUT,

        sock_read=SOCK_READ_TIMEOUT

    )

    connector = aiohttp.TCPConnector(
        ssl=True,
        limit=100
    )

    logger.info(f"Download requested: {url}")

    started = time.time()

    try:

        async with aiohttp.ClientSession(

            timeout=timeout,

            headers=DEFAULT_HEADERS,

            connector=connector,

        ) as session:

            async with session.get(

                url,

                allow_redirects=True,

                max_redirects=MAX_REDIRECTS,

            ) as response:

                if response.status != 200:

                    raise HTTPException(

                        status_code=response.status,

                        detail=f"Remote server returned {response.status}"

                    )

                # -------------------------
                # Content Length
                # -------------------------

                content_length = response.headers.get(
                    "Content-Length"
                )

                if content_length:

                    size = int(content_length)

                    if size > MAX_FILE_SIZE:

                        raise HTTPException(

                            status_code=413,

                            detail="File is larger than allowed limit."

                        )

                downloaded = 0

                with open(filepath, "wb") as f:

                    async for chunk in response.content.iter_chunked(
                        CHUNK_SIZE
                    ):

                        if not chunk:
                            continue

                        downloaded += len(chunk)

                        if downloaded > MAX_FILE_SIZE:

                            raise HTTPException(

                                status_code=413,

                                detail="Maximum file size exceeded."

                            )

                        f.write(chunk)

                final_size = os.path.getsize(filepath)

                elapsed = round(
                    time.time() - started,
                    2
                )

                logger.info(

                    f"Download finished | "

                    f"{filename} | "

                    f"{final_size} bytes | "

                    f"{elapsed}s"

                )

                return {

                    "status": "downloaded",

                    "filename": filename,

                    "size": final_size,

                    "path": filepath,

                    "elapsed": elapsed,

                }

    # --------------------------
    # Timeouts
    # --------------------------

    except asyncio.TimeoutError:

        logger.error("Download timeout")

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(

            status_code=408,

            detail="Download timeout."

        )

    # --------------------------
    # Connection Error
    # --------------------------

    except aiohttp.ClientConnectorError:

        logger.error("Cannot connect")

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(

            status_code=502,

            detail="Cannot connect to remote host."

        )

    # --------------------------
    # Invalid SSL
    # --------------------------

    except aiohttp.ClientSSLError:

        logger.error("SSL Error")

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(

            status_code=495,

            detail="SSL validation failed."

        )

    # --------------------------
    # HTTP Exception
    # --------------------------

    except HTTPException:

        if os.path.exists(filepath):
            os.remove(filepath)

        raise

    # --------------------------
    # Any Other Error
    # --------------------------

    except Exception as e:

        logger.exception(str(e))

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(

            status_code=500,

            detail="Internal server error."

        )

    finally:

        if 'connector' in locals():
            await connector.close()