import httpx
import yndx_disk.api.utils as utils


BASE_URL = "https://cloud-api.yandex.net/v1/disk/operations"


async def get_operation_status(token: str, operation_id: str, fields: str = "", timeout: int = 30) -> httpx.Response:
    """
    Get the status of an operation on the server.

    Parameters:
    - token (str): The authentication token for the server.
    - operation_id (str): The ID of the operation to get the status for.
    - fields (str, optional): The fields to be included in the response. Defaults to "".
    - timeout (int, optional): The timeout for the request in seconds. Defaults to 30.

    Returns:
    - httpx.Response: The response from the server containing the status of the operation.
    """
    url = BASE_URL + f"/{operation_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "operation_id": operation_id,
                "fields": fields,
            },
            timeout=timeout
        )

    return response

