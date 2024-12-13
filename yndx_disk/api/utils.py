from pathlib import Path


DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Authorization": "OAuth {token}",
}



def generate_headers(token: str) -> dict:
    headers = DEFAULT_HEADERS.copy()

    headers["Authorization"] = f"OAuth {token}"

    return headers


def parse_path(path: str) -> str:
    if path.startswith("/"):
        path = "disk:/" + path[1:]
    elif not path.startswith("disk:/"):
        path = "disk:/" + path

    path = Path(path)   # Some kind of check is path valid or not =P

    return str(path)


