import asyncio
from aiohttp import ClientSession

from yndx_disk.classes import File, Directory
from yndx_disk.clients.async_client import AsyncDiskClient


class DiskClient(AsyncDiskClient):
    def __init__(self, token: str, auto_update_info: bool = True, session: ClientSession = None):
        if not session:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            session = ClientSession(loop=self._loop)

        super().__init__(token, auto_update_info, session=session)

    def _cleanup(self) -> None:
        self._loop.run_until_complete(self.session.close())

    def update_disk_info(self) -> None:
        return self._loop.run_until_complete(super().update_disk_info())

    def get_object(self, path: str) -> File | Directory:
        return self._loop.run_until_complete(super().get_object(path))

    def listdir(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        return self._loop.run_until_complete(super().listdir(path, limit, offset))

    def delete(self, path: str = "", permanently: bool = False) -> None:
        return self._loop.run_until_complete(super().delete(path, permanently))

    def move(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        return self._loop.run_until_complete(super().move(source_path, destination_path, overwrite))

    def copy(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        return self._loop.run_until_complete(super().copy(source_path, destination_path, overwrite))

    def publish(self, path: str, return_public_url: bool = False) -> str | None:
        return self._loop.run_until_complete(super().publish(path, return_public_url))

    def unpublish(self, path: str):
        return self._loop.run_until_complete(super().unpublish(path))

    def upload_file(self, file_path: str, path: str, overwrite: bool = False, chunk_size: int = 1024) -> None:
        return self._loop.run_until_complete(super().upload_file(file_path, path, overwrite, chunk_size))

    def get_url(self, path: str = "/") -> str:
        return self._loop.run_until_complete(super().get_url(path))

    def listdir_trash(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        return self._loop.run_until_complete(super().listdir_trash(path, limit, offset))

    def delete_trash(self, path: str = ""):
        return self._loop.run_until_complete(super().delete_trash(path))

    def restore_trash(self, path: str, new_name: str = "", overwrite: bool = False):
        return self._loop.run_until_complete(super().restore_trash(path, new_name, overwrite))
