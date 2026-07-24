from pathlib import Path

from rubpy import Client


SESSION_NAME = str(
    Path("sessions") / "time_sessions"
)


def get_client():

    return Client(SESSION_NAME)