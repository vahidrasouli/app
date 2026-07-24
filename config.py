import os

# ------------------------
# Application
# ------------------------

APP_NAME = "Rubika Uploader"
APP_VERSION = "1.0.0"

# ------------------------
# Download
# ------------------------

DOWNLOAD_DIR = "/tmp"

CHUNK_SIZE = 1024 * 1024  # 1MB

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

# ------------------------
# Network
# ------------------------

CONNECT_TIMEOUT = 15

SOCK_READ_TIMEOUT = 600

TOTAL_TIMEOUT = 900

MAX_REDIRECTS = 5

USER_AGENT = "RubikaUploader/1.0"

# ------------------------
# Logging
# ------------------------

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(message)s"
)

# ------------------------
# Security
# ------------------------

ALLOWED_SCHEMES = (
    "http",
    "https",
)

# Private / Reserved Networks

BLOCKED_NETWORKS = [

    "127.0.0.0/8",

    "10.0.0.0/8",

    "172.16.0.0/12",

    "192.168.0.0/16",

    "169.254.0.0/16",

    "0.0.0.0/8",

    "100.64.0.0/10",

    "224.0.0.0/4",

    "240.0.0.0/4",

    "::1/128",

    "fc00::/7",

    "fe80::/10",
]

# ------------------------
# HTTP
# ------------------------

DEFAULT_HEADERS = {

    "User-Agent": USER_AGENT,

    "Accept": "*/*",

    "Connection": "keep-alive",
}

# ------------------------
# Runtime
# ------------------------

os.makedirs(DOWNLOAD_DIR, exist_ok=True)