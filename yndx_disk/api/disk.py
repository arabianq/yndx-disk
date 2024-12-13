import httpx
import yndx_disk.api.utils as utils


BASE_URL = "https://cloud-api.yandex.net/v1/disk"


async def get_disk_info(token: str, fields: str = "", timeout: int = 30) -> httpx.Response:
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

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "fields": fields,
            },
            timeout=timeout
        )

    return response
