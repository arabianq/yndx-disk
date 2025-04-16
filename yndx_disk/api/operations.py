from aiohttp import ClientSession, ClientResponse

import yndx_disk.api.utils as utils

BASE_URL = "https://cloud-api.yandex.net/v1/disk/operations"


async def get_operation_status(token: str, operation_id: str, session: ClientSession = None, fields: str = "",
                               timeout: int = 30) -> ClientResponse:
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

    close_session = False
    if not session:
        session = ClientSession()
        close_session = True

    response = await session.get(
        url=url,
        headers=utils.generate_headers(token=token),
        params={
            "operation_id": operation_id,
            "fields": fields,
        },
        timeout=timeout
    )

    if close_session:
        await session.close()

    return response
