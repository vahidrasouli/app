from pathlib import Path
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