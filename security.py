import ipaddress
import os
import re
import socket
import uuid
from urllib.parse import urlparse, unquote

from fastapi import HTTPException

from config import ALLOWED_SCHEMES, BLOCKED_NETWORKS


# ------------------------
# Blocked Networks
# ------------------------

BLOCKED_IPS = [
    ipaddress.ip_network(net)
    for net in BLOCKED_NETWORKS
]


# ------------------------
# Filename
# ------------------------

INVALID_CHARS = re.compile(r"[^A-Za-z0-9._-]")


def generate_safe_filename(url: str) -> str:
    """
    Generate a safe filename from URL.
    """

    parsed = urlparse(url)

    filename = os.path.basename(unquote(parsed.path))

    if not filename:
        filename = "download.bin"

    filename = INVALID_CHARS.sub("_", filename)

    filename = filename.strip("._")

    if not filename:
        filename = "download.bin"

    return f"{uuid.uuid4().hex[:12]}_{filename}"


# ------------------------
# URL Validation
# ------------------------

def validate_url(url: str) -> str:

    parsed = urlparse(url)

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise HTTPException(
            status_code=400,
            detail="Only http and https are allowed."
        )

    if not parsed.hostname:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )

    return parsed.hostname


# ------------------------
# Resolve Host
# ------------------------

def resolve_host(host: str):

    try:
        return socket.getaddrinfo(
            host,
            None,
            proto=socket.IPPROTO_TCP
        )

    except socket.gaierror:

        raise HTTPException(
            status_code=400,
            detail="Cannot resolve hostname."
        )


# ------------------------
# SSRF Protection
# ------------------------

def validate_host(host: str):

    addresses = resolve_host(host)

    for addr in addresses:

        ip = addr[4][0]

        try:
            ip_obj = ipaddress.ip_address(ip)

        except ValueError:
            continue

        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_reserved
            or ip_obj.is_multicast
            or ip_obj.is_link_local
            or ip_obj.is_unspecified
        ):
            raise HTTPException(
                status_code=403,
                detail=f"Blocked address: {ip}"
            )

        for network in BLOCKED_IPS:

            if ip_obj in network:

                raise HTTPException(
                    status_code=403,
                    detail=f"Blocked address: {ip}"
                )


# ------------------------
# Public API
# ------------------------

def validate_download_url(url: str):

    host = validate_url(url)

    validate_host(host)

    return True