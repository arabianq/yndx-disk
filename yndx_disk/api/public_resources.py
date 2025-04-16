from aiohttp import ClientSession, ClientResponse

import yndx_disk.api.utils as utils

BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"


async def get_info(token: str, public_key: str, session: ClientSession = None, fields: str = "", path: str = "",
                   preview_size: str = "", sort: str = "", preview_crop: bool = False, limit: int = 100,
                   offset: int = 0, timeout: int = 30) -> ClientResponse:
    """
    Get information about a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - public_key (str): The public key of the file or directory to get information about.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - path (str, optional): The path of the file or directory to get information about. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - sort (str, optional): The sorting order of the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server containing the information about the file or directory.
    """
    url = BASE_URL

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    preview_crop = "true" if preview_crop else "false"

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "public_key": public_key,
            "fields": fields,
            "path": utils.parse_path(path),
            "preview_size": preview_size,
            "sort": sort,
            "preview_crop": preview_crop,
            "limit": limit,
            "offset": offset,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def get_url(token: str, public_key: str, session: ClientSession = None, fields: str = "", path: str = "",
                  timeout: int = 30) -> ClientResponse:
    """
    Get the download URL for a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - public_key (str): The public key of the file or directory to get the download URL for.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - path (str, optional): The path of the file or directory to get the download URL for. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server containing the download URL for the file or directory.
    """
    url = BASE_URL + "/download"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "public_key": public_key,
            "fields": fields,
            "path": utils.parse_path(path),
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def save_to_disk(token: str, public_key: str, session: ClientSession = None, fields: str = "", name: str = "",
                       path: str = "", save_path: str = "", force_async: bool = False,
                       timeout: int = 30) -> ClientResponse:
    """
    Save a file or directory from the disk to your own disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - public_key (str): The public key of the file or directory to be saved.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - name (str, optional): The name of the file or directory to be saved. Defaults to "".
    - path (str, optional): The path of the file or directory to be saved. Defaults to "".
    - save_path (str, optional): The path where the file or directory should be saved to. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous saving. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server after the save operation.
    """
    url = BASE_URL + "/save-to-disk"

    force_async = "true" if force_async else "false"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.post(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "public_key": public_key,
            "fields": fields,
            "name": name,
            "path": utils.parse_path(path),
            "save_path": save_path,
            "force_async": force_async,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response
