from aiohttp import ClientSession, ClientResponse

import yndx_disk.api.utils as utils

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


async def delete(token: str, path: str, session: ClientSession = None, fields: str = "", md5: str = "",
                 force_async: bool = False, permanently: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Delete a file or directory from the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to be deleted.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - md5 (str, optional): The MD5 hash of the file to be deleted. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous deletion. Defaults to False.
    - permanently (bool, optional): Whether to delete the file permanently. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the deletion operation.
    """
    url = BASE_URL

    if not session:
        session = ClientSession()

    force_async = "true" if force_async else "false"
    permanently = "true" if permanently else "false"

    response = await session.delete(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "fields": fields,
            "md5": md5,
            "force_async": force_async,
            "permanently": permanently,
        },
        timeout=timeout
    )

    return response


async def get_info(token: str, path: str, session: ClientSession = None, fields: str = "", preview_size: str = "",
                   sort: str = "", preview_crop: str = False, limit: int = 100, offset: int = 0,
                   timeout: int = 30) -> ClientResponse:
    """
    Get information about a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to get information about.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - sort (str, optional): The sorting order of the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing the information about the file or directory.
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
            "path": utils.parse_path(path),
            "fields": fields,
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


async def update_info(token: str, path: str, body: dict, session: ClientSession = None, fields: str = "",
                      timeout: int = 30) -> ClientResponse:
    """
    Update information about a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to update.
    - body (dict): The new information to be updated.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the update operation.
    """
    url = BASE_URL

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.patch(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "body": body,
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def mkdir(token: str, path: str, session: ClientSession = None, fields: str = "",
                timeout: int = 30) -> ClientResponse:
    """
    Create a new directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the new directory to be created.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the creation operation.
    """
    url = BASE_URL

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.put(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def copy(token: str, from_path: str, to_path: str, session: ClientSession = None, fields: str = "",
               force_async: bool = False, overwrite: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Copy a file or directory from one location to another on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - from_path (str): The path of the file or directory to be copied.
    - to_path (str): The path where the file or directory should be copied to.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous copying. Defaults to False.
    - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the copy operation.
    """
    url = BASE_URL + "/copy"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    force_async = "true" if force_async else "false"
    overwrite = "true" if overwrite else "false"

    response = await session.post(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "from": utils.parse_path(from_path),
            "path": utils.parse_path(to_path),
            "fields": fields,
            "force_async": force_async,
            "overwrite": overwrite,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def get_url(token: str, path: str, session: ClientSession = None, fields: str = "",
                  timeout: int = 30) -> ClientResponse:
    """
    Get the download URL for a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to get the download URL for.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing the download URL for the file or directory.
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
            "path": utils.parse_path(path),
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def get_all_files(token: str, session: ClientSession = None, fields: str = "", media_type: str = "",
                        preview_size: str = "", sort: str = "", preview_crop: bool = False, limit: int = 100,
                        offset: int = 0, timeout: int = 30) -> ClientResponse:
    """
    Get a list of all files and directories on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - media_type (str, optional): The media type of the files to be included in the response. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - sort (str, optional): The sorting order of the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing a list of all files and directories.
    """
    url = BASE_URL + "/files"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    preview_crop = "true" if preview_crop else "false"

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "fields": fields,
            "media_type": media_type,
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


async def get_last_uploads(token: str, session: ClientSession = None, fields: str = "", media_type: str = "",
                           preview_size: str = "", preview_crop: bool = False, limit: int = 100,
                           timeout: int = 30) -> ClientResponse:
    """
    Get a list of the last uploaded files and directories on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - media_type (str, optional): The media type of the files to be included in the response. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing a list of the last uploaded files and directories.
    """
    url = BASE_URL + "/last-uploaded"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    preview_crop = "true" if preview_crop else "false"

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "fields": fields,
            "media_type": media_type,
            "preview_size": preview_size,
            "preview_crop": preview_crop,
            "limit": limit,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def move(token: str, from_path: str, to_path: str, session: ClientSession = None, fields: str = "",
               force_async: bool = False, overwrite: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Move a file or directory from one location to another on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - from_path (str): The path of the file or directory to be moved.
    - to_path (str): The path where the file or directory should be moved to.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - force_async (bool, optional): Whether to force asynchronous moving. Defaults to False.
    - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the move operation.
    """
    url = BASE_URL + "/move"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    force_async = "true" if force_async else "false"
    overwrite = "true" if overwrite else "false"

    response = await session.post(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "from": utils.parse_path(from_path),
            "path": utils.parse_path(to_path),
            "fields": fields,
            "force_async": force_async,
            "overwrite": overwrite,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def get_all_public(token: str, session: ClientSession = None, fields: str = "", preview_size: str = "",
                         type_filter: str = "", preview_crop: bool = False, limit: int = 100, offset: int = 0,
                         timeout: int = 30) -> ClientResponse:
    """
    Get a list of all public files and directories on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - preview_size (str, optional): The size of the preview to be included in the response. Defaults to "".
    - type_filter (str, optional): The type of files to be included in the response. Defaults to "".
    - preview_crop (bool, optional): Whether to crop the preview. Defaults to False.
    - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
    - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing a list of all public files and directories.
    """
    url = BASE_URL + "/public"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    preview_crop = "true" if preview_crop else "false"

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "fields": fields,
            "preview_size": preview_size,
            "type_filter": type_filter,
            "preview_crop": preview_crop,
            "limit": limit,
            "offset": offset,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def publish(token: str, path: str, body: dict, session: ClientSession = None, fields: str = "",
                  allow_address_access: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Publish a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to be published.
    - body (dict): The information to be published.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - allow_address_access (bool, optional): Whether to allow address access. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the publish operation.
    """
    url = BASE_URL + "/publish"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    allow_address_access = "true" if allow_address_access else "false"

    response = await session.put(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "body": body,
            "fields": fields,
            "allow_address_access": allow_address_access,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def unpublish(token: str, path: str, session: ClientSession = None, fields: str = "",
                    timeout: int = 30) -> ClientResponse:
    """
    Unpublish a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to be unpublished.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the unpublish operation.
    """
    url = BASE_URL + "/unpublish"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.put(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def get_upload_url(token: str, path: str, session: ClientSession = None, fields: str = "",
                         overwrite: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Get the upload URL for a file or directory on the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path of the file or directory to get the upload URL for.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - overwrite (bool, optional): Whether to overwrite the file or directory if it already exists. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server containing the upload URL for the file or directory.
    """
    url = BASE_URL + "/upload"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    overwrite = "true" if overwrite else "false"

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "fields": fields,
            "overwrite": overwrite,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response


async def upload(token: str, path: str, upload_url: str, session: ClientSession = None, fields: str = "",
                 disable_redirects: bool = False, timeout: int = 30) -> ClientResponse:
    """
    Upload a file or directory to the disk.

    Parameters:
    - token (str): The authentication token for the disk.
    - path (str): The path where the file or directory should be uploaded.
    - upload_url (str): The URL to upload the file or directory to.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - disable_redirects (bool, optional): Whether to disable redirects. Defaults to False.
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - ClientResponse: The response from the server after the upload operation.
    """
    url = BASE_URL + "/upload"

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    disable_redirects = "true" if disable_redirects else "false"

    response = await session.post(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "path": utils.parse_path(path),
            "url": upload_url,
            "fields": fields,
            "disable_redirects": disable_redirects,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response
