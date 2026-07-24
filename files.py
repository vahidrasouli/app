from pathlib import Path
from fastapi import HTTPException
from datetime import datetime

from config import DOWNLOAD_DIR


def list_files():

    directory = Path(DOWNLOAD_DIR)

    if not directory.exists():
        return {
            "count": 0,
            "files": []
        }

    files = []

    for file in sorted(
        directory.iterdir(),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    ):

        if not file.is_file():
            continue

        stat = file.stat()

        files.append({

            "filename": file.name,

            "size": stat.st_size,

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "path": str(file)

        })

    return {

        "count": len(files),

        "files": files

    }


def get_file(filename: str):

    file = Path(DOWNLOAD_DIR) / filename

    if not file.exists() or not file.is_file():
        return None

    stat = file.stat()

    return {
        "filename": file.name,
        "size": stat.st_size,
        "path": str(file),
        "created": stat.st_ctime,
        "modified": stat.st_mtime
    }


def delete_file(filename: str):

    file = Path(DOWNLOAD_DIR) / filename

    if not file.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    file.unlink()

    return {
        "status": "deleted",
        "filename": filename
    }


def delete_all_files():

    directory = Path(DOWNLOAD_DIR)

    deleted = []

    if not directory.exists():

        return {
            "deleted": 0,
            "files": []
        }

    for file in directory.iterdir():

        if not file.is_file():
            continue

        deleted.append(file.name)

        file.unlink()

    return {

        "deleted": len(deleted),

        "files": deleted

    }