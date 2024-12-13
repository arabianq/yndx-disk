import httpx
import yndx_disk.api.utils as utils


BASE_URL = "https://cloud-api.yandex.net/v1/disk/trash/resources"


async def delete(token: str, fields: str = "", path: str = "", force_async: bool = False, timeout: int = 30) -> httpx.Response:
    """
    Empty the trash on the server.

    Parameters:
    - token (str): The authentication token for the server.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - path (str, optional): The path of the trash to be emptied. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous emptying. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server after the emptying operation.
    """
    url = BASE_URL

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "fields": fields,
                "path": "" if not path else utils.parse_path(path, "trash:/"),
                "force_async": force_async,
            },
            timeout=timeout
        )

    return response



async def get_info(token: str, path: str, fields: str = "", preview_size: str = "", sort: str = "",
                            preview_crop: bool = False, limit: int = 100, offset: int = 0, timeout: int = 30) -> httpx.Response:
    """
    Get the content of the trash on the server.

    Parameters:
    - token (str): The authentication token for the server.
    - path (str): The path of the trash to get the content from.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - sort (str, optional): The sorting order of the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server containing the content of the trash.
    """
    url = BASE_URL

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "path": "" if not path else utils.parse_path(path, "trash:/"),
                "fields": fields,
                "preview_size": preview_size,
                "sort": sort,
                "preview_crop": preview_crop,
                "limit": limit,
                "offset": offset,
            },
            timeout=timeout
        )

    return response


async def restore(token: str, path: str, fields: str = "", name: str = "", force_async: bool = False,
                  overwrite: bool = False, timeout: int = 30) -> httpx.Response:
    """
    Restore a file or directory from the trash on the server.

    Parameters:
    - token (str): The authentication token for the server.
    - path (str): The path of the file or directory to be restored.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - name (str, optional): The name of the file or directory to be restored. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous restoring. Defaults to False.
    - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server after the restore operation.
    """
    url = BASE_URL + "/restore"

    async with httpx.AsyncClient() as client:
        response = await client.put(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "path": "" if not path else utils.parse_path(path, "trash:/"),
                "fields": fields,
                "name": name,
                "force_async": force_async,
                "overwrite": overwrite,
            },
            timeout=timeout
        )

    return response

