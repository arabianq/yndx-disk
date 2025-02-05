from yndx_disk.classes import File, Directory
from yndx_disk.clients.async_client import AsyncDiskClient

import asyncio


class DiskClient(AsyncDiskClient):
    def __init__(self, token: str, auto_update_info: bool = True):
        super().__init__(token, auto_update_info)

    def update_disk_info(self) -> None:
        return asyncio.run(super().update_disk_info())

    def get_object(self, path: str) -> File | Directory:
        return asyncio.run(super().get_object(path))

    def listdir(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        return asyncio.run(super().listdir(path, limit, offset))

    def delete(self, path: str = "", permanently: bool = False) -> None:
        return asyncio.run(super().delete(path, permanently))

    def move(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        return asyncio.run(super().move(source_path, destination_path, overwrite))

    def copy(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        return asyncio.run(super().copy(source_path, destination_path, overwrite))

    def publish(self, path: str, return_public_url: bool = False) -> str | None:
        return asyncio.run(super().publish(path, return_public_url))

    def unpublish(self, path: str):
        return asyncio.run(super().unpublish(path))

    def upload_file(self, file_path: str, path: str, overwrite: bool = False, chunk_size: int = 1024) -> None:
        return asyncio.run(super().upload_file(file_path, path, overwrite, chunk_size))

    def get_url(self, path: str = "/") -> str:
        return asyncio.run(super().get_url(path))

    def listdir_trash(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        return asyncio.run(super().listdir_trash(path, limit, offset))

    def delete_trash(self, path: str = ""):
        return asyncio.run(super().delete_trash(path))

    def restore_trash(self, path: str, new_name: str = "", overwrite: bool = False):
        return asyncio.run(super().restore_trash(path, new_name, overwrite))



