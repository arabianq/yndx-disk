from pathlib import Path

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Authorization": "OAuth {token}",
}


def generate_headers(token: str) -> dict:
    headers = DEFAULT_HEADERS.copy()

    headers["Authorization"] = f"OAuth {token}"

    return headers


def parse_path(path: str, prefix: str = "disk:/") -> str:
    path = str(Path(path))  # Some kind of check is path valid or not =P

    if path.startswith("/"):
        path = prefix + path[1:]
    elif not path.startswith(prefix):
        path = prefix + path

    return path
