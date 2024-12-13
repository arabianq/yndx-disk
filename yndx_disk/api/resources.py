import asyncio
import httpx
import yndx_disk.utils as utils
import yndx_disk.exceptions as exceptions

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


async def delete(token: str, path: str, fields: str = "", md5: str = "", force_async: bool = False,
                 permanently: bool = False, timeout: int = 30):
    url = BASE_URL

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "path": path,
                "fields": fields,
                "md5": md5,
                "force_async": force_async,
                "permanently": permanently,
            },
            timeout=timeout
        )

    response_json = response.json()

    match response.status_code:
        case 200:
            return response_json
        case _:
            raise exceptions.YandexDiskAPIException(response.status_code, response_json.get("description", ""))


async def get_info(token: str, path: str, fields: str = "", preview_size: str = "", sort: str = "",
                   preview_crop: bool = False, limit: int = 100, offset: int = 0, timeout: int = 30):
    url = BASE_URL

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            headers=utils.generate_headers(token=token),
            params={
                "path": path,
                "fields": fields,
                "preview_size": preview_size,
                "sort": sort,
                "preview_crop": preview_crop,
                "limit": limit,
                "offset": offset,
            },
            timeout=timeout
        )

    response_json = response.json()

    match response.status_code:
        case 200:
            return response_json
        case _:
            raise exceptions.YandexDiskAPIException(response.status_code, response_json.get("description", ""))

async def update_info(token: str, path: str, body: dict, fields: str = "", timeout: int = 30):
    url = BASE_URL

async def mkdir(token: str, path: str, fields: str = "", timeout: int = 30):
    url = BASE_URL

async def copy(token: str, from_path: str, to_path: str, fields: str = "", force_async: bool = False,
               overwrite: bool = False, timeout: int = 30):
    url = BASE_URL + "/copy"

async def get_url(token: str, path: str, fields: str = "", timeout: int = 30):
    url = BASE_URL + "/download"

async def get_all_files(token: str, fields: str = "", media_type: str = "", preview_size: str = "", sort: str = "",
                        preview_crop: bool = False, limit: int = 100, offset: int = 0, timeout: int = 30):
    url = BASE_URL + "/files"

async def get_last_uploads(token: str, fields: str = "", media_type: str = "", preview_size: str = "",
                           preview_crop: bool = False, limit: int = 100, timeout: int = 30):
    url = BASE_URL + "/last-uploaded"

async def move(token: str, from_path: str, to_path: str, fields: str = "", force_async: bool = False,
               overwrite: bool = False, timeout: int = 30):
    url = BASE_URL + "/move"

async def get_all_public(token: str, fields: str = "", preview_size: str = "", type_filter: str = "",
                         preview_crop: bool = False, limit: int = 100, offset: int = 0, timeout: int = 30):
    url = BASE_URL + "/public"

async def publish(token: str, path: str, body: dict, fields: str = "", allow_address_access: bool = False,
                  timeout: int = 30):
    url = BASE_URL + "/publish"

async def unpublish(token: str, path: str, fields: str = "", timeout: int = 30):
    url = BASE_URL + "/unpublish"

async def get_upload_url(token: str, path: str, fields: str = "", overwrite: bool = False, timeout: int = 30):
    url = BASE_URL + "/upload"

async def upload(token: str, upload_url: str, fields: str = "", disable_redirects: bool = False, timeout: int = 30):
    url = BASE_URL + "/upload"