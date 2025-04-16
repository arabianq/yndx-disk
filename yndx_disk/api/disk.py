from aiohttp import ClientSession, ClientResponse

import yndx_disk.api.utils as utils

BASE_URL = "https://cloud-api.yandex.net/v1/disk"


async def get_disk_info(token: str, session: ClientSession = None, fields: str = "",
                        timeout: int = 30) -> ClientResponse:
    """
    Get information about the disk.

    Parameters:
    - token (str): The authentication token for the server.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server containing the disk information.
    """
    url = BASE_URL

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response
