from aiohttp import ClientSession

import yndx_disk.api.disk as api_disk
import yndx_disk.api.resources as api_resources
import yndx_disk.api.operations as api_operations
import yndx_disk.api.trash_resources as api_trash_resources
import yndx_disk.api.public_resources as api_public_resources
import yndx_disk.api.exceptions as api_exceptions
from yndx_disk.api.utils import parse_path

from yndx_disk.classes import File, Directory

import asyncio
import aiofiles
import os
import atexit


class AsyncDiskClient:
    """
    A class representing an asynchronous client for interacting with a disk service.

    Attributes:
    - user (dict): Information about the user.
    - system_folders (dict): Information about the system folders.
    - is_paid (bool): Whether the user has a paid account.
    - payment_flow (bool): Whether the user is in the payment flow.
    - unlimited_autoupload_enabled (bool): Whether unlimited autoupload is enabled.
    - reg_time (str): The registration time of the user.
    - total_space (int): The total disk space available.
    - used_space (int): The used disk space.
    - max_file_size (int): The maximum file size allowed.
    - paid_max_file_size (int): The maximum file size allowed for a paid account.
    - photounlim_size (int): The photo unlimited size.
    - trash_size (int): The size of the trash.
    - revision (int): The revision number.
    """
    user: dict = None
    system_folders: dict = None

    is_paid: bool = None
    payment_flow: bool = None
    unlimited_autoupload_enabled: bool = None

    reg_time: str = None

    total_space: int = None
    used_space: int = None

    max_file_size: int = None
    paid_max_file_size: int = None
    photounlim_size: int = None
    trash_size: int = None

    revision: int = None

    session: ClientSession = None

    def __init__(self, token: str, auto_update_info: bool = True, session: ClientSession = None):
        """
        Initialize an instance of the AsyncDiskClient class.

        Parameters:
        - token (str): The authentication token for the server.
        - auto_update_info (bool, optional): Whether to automatically update the client's information. Defaults to True.

        Returns:
        - None
        """
        self.token = token
        self.auto_update_info = auto_update_info

        if not session:
            loop = asyncio.get_running_loop()
            session = ClientSession(loop=loop)
        self.session = session

        atexit.register(self._cleanup)

    def _cleanup(self) -> None:
        """
        Cleanup on exit.
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.session.close())

    def __del__(self) -> None:
        self._cleanup()

    async def _wait_for_operation_to_finish(self, operation_id: str) -> bool:
        """
        Wait for an operation to finish.

        This method continuously checks the status of an operation until it is no longer in progress. If the operation fails, the method returns False. Otherwise, it returns True.

        Parameters:
        - operation_id (str): The ID of the operation to wait for.

        Returns:
        - bool: True if the operation is successful, False otherwise.
        """
        operation_status_response = await api_operations.get_operation_status(token=self.token,
                                                                              operation_id=operation_id,
                                                                              session=self.session)
        operation_status_response_json = await operation_status_response.json()
        operation_status = False if operation_status_response_json.get("status", "") == "in-progress" else True

        while not operation_status:
            operation_status_response = await api_operations.get_operation_status(self.token, operation_id,
                                                                                  self.session)
            operation_status_response_json = await operation_status_response.json()
            operation_status = False if operation_status_response_json.get("status", "") == "in-progress" else True

            await asyncio.sleep(0.1)

        if operation_status_response_json.get("status", "") == "failed":
            return False

        return True

    async def update_disk_info(self) -> None:
        """
        Update the disk information for the client.

        This method retrieves the disk information from the server using the provided token. If the request is successful (status code 200), it updates the client's information with the retrieved data. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

        Returns:
        - None
        """
        response = await api_disk.get_disk_info(token=self.token, session=self.session)
        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        self.user = response_json.get("user", {})
        self.system_folders = response_json.get("system_folders", {})

        self.is_paid = response_json.get("is_paid", False)
        self.payment_flow = response_json.get("payment flow", False)
        self.unlimited_autoupload_enabled = response_json.get("unlimited_autoupload_enabled", False)

        self.reg_time = response_json.get("reg_time", "")

        self.total_space = response_json.get("total_space", 0)
        self.used_space = response_json.get("used_space", 0)

        self.max_file_size = response_json.get("max_file_size", 0)
        self.paid_max_file_size = response_json.get("max_file_size", 0)
        self.photounlim_size = response_json.get("photounlim_size", 0)
        self.trash_size = response_json.get("trash_size", 0)

        self.revision = response_json.get("revision", 0)

    async def get_object(self, path: str) -> File | Directory:
        """
            Get an object from the disk.

            This method retrieves information about an object (file or directory) from the disk using the provided path. If the request is successful (status code 200), it returns a File or Directory object based on the type of the object. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str): The path of the object to retrieve.

            Returns:
            - File | Directory: The retrieved File or Directory object.

            Raises:
            - YandexDiskAPIException: If the request fails or if the object type cannot be determined.
            """
        response = await api_resources.get_info(token=self.token, path=path, session=self.session, limit=0)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        object_type = response_json.get("type", "")

        match object_type:
            case "file":
                return File(
                    token=self.token,
                    created_at=response_json.get("created", ""),
                    modified_at=response_json.get("modified", ""),
                    name=response_json.get("name", ""),
                    path=response_json.get("path", ""),
                    resource_id=response_json.get("resource_id", ""),
                    revision=response_json.get("revision", 0),
                    public_key=response_json.get("public_key", ""),
                    public_url=response_json.get("public_url", ""),
                    antivirus_status=response_json.get("antivirus_status", ""),
                    file_url=response_json.get("file", ""),
                    preview_url=response_json.get("preview", ""),
                    md5=response_json.get("md5", ""),
                    sha256=response_json.get("sha256", ""),
                    media_type=response_json.get("media_type", ""),
                    mime_type=response_json.get("mime_type", ""),
                    size=response_json.get("size", 0),
                )
            case "dir":
                return Directory(
                    token=self.token,
                    created_at=response_json.get("created", ""),
                    modified_at=response_json.get("modified", ""),
                    name=response_json.get("name", ""),
                    path=response_json.get("path", ""),
                    resource_id=response_json.get("resource_id", ""),
                    revision=response_json.get("revision", 0),
                    public_key=response_json.get("public_key", ""),
                    public_url=response_json.get("public_url", ""),
                )
            case _:
                raise api_exceptions.YandexDiskAPIException(f"Could not determine object type {path}")

    async def listdir(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        """
            List the contents of a directory on the disk.

            This method retrieves the contents of a directory from the disk using the provided path. If the request is successful (status code 200), it returns a list of File or Directory objects representing the contents of the directory. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str, optional): The path of the directory to list. Defaults to "/".
            - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
            - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.

            Returns:
            - list[File | Directory]: A list of File or Directory objects representing the contents of the directory.

            Raises:
            - YandexDiskAPIException: If the request fails or if the object type cannot be determined.
            """
        response = await api_resources.get_info(token=self.token, session=self.session, path=path, limit=limit,
                                                offset=offset)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        embedded_items = response_json.get("_embedded", {}).get("items", [])
        directory_contents = []

        for item in embedded_items:
            item_type = item.get("type", "")
            if not item_type:
                continue

            match item_type:
                case "file":
                    directory_contents.append(
                        File(
                            token=self.token,
                            created_at=item.get("created", ""),
                            modified_at=item.get("modified", ""),
                            name=item.get("name", ""),
                            path=item.get("path", ""),
                            resource_id=item.get("resource_id", ""),
                            revision=item.get("revision", 0),
                            public_key=item.get("public_key", ""),
                            public_url=item.get("public_url", ""),
                            antivirus_status=item.get("antivirus_status", ""),
                            file_url=item.get("file", ""),
                            preview_url=item.get("preview", ""),
                            md5=item.get("md5", ""),
                            sha256=item.get("sha256", ""),
                            media_type=item.get("media_type", ""),
                            mime_type=item.get("mime_type", ""),
                            size=item.get("size", 0),
                        )
                    )
                case "dir":
                    directory_contents.append(
                        Directory(
                            token=self.token,
                            created_at=item.get("created", ""),
                            modified_at=item.get("modified", ""),
                            name=item.get("name", ""),
                            path=item.get("path", ""),
                            resource_id=item.get("resource_id", ""),
                            revision=item.get("revision", 0),
                            public_key=item.get("public_key", ""),
                            public_url=item.get("public_url", ""),
                        )
                    )
                case _:
                    continue

        return directory_contents

    async def delete(self, path: str, permanently: bool = False) -> None:
        """
            Delete a file or directory from the disk.

            This method deletes a file or directory from the disk using the provided path. If the request is successful (status code 202), it waits for the operation to finish and raises a YandexDiskAPIException if the operation fails. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response. If the auto_update_info attribute is True, it updates the disk information after the operation is successful.

            Parameters:
            - path (str): The path of the file or directory to be deleted.
            - permanent (bool, optional): Whether to delete the file or directory permanently. Defaults to False.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails or if the operation fails.
            """
        response = await api_resources.delete(token=self.token, session=self.session, path=path, force_async=True,
                                              permanently=permanently)

        response_json = await response.json()

        if response.status != 202:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        href = response_json.get("href", "")
        operation_id = href.split("/")[-1]
        operation_status = await self._wait_for_operation_to_finish(operation_id)

        if not operation_status:
            raise api_exceptions.YandexDiskAPIException(f"Failed to delete {path}.")

        if self.auto_update_info:
            await self.update_disk_info()

    async def move(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        """
            Move a file or directory from one location to another on the disk.

            This method moves a file or directory from the source path to the destination path. If the request is successful (status code 202), it waits for the operation to finish and raises a YandexDiskAPIException if the operation fails. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response. If the auto_update_info attribute is True, it updates the disk information after the operation is successful.

            Parameters:
            - source_path (str): The path of the file or directory to be moved.
            - destination_path (str): The path where the file or directory should be moved to.
            - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails or if the operation fails.
            """
        response = await api_resources.move(token=self.token, session=self.session, from_path=source_path,
                                            to_path=destination_path, force_async=True, overwrite=overwrite)

        response_json = await response.json()

        if response.status != 202:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        href = response_json.get("href", "")
        operation_id = href.split("/")[-1]
        operation_status = await self._wait_for_operation_to_finish(operation_id)

        if not operation_status:
            raise api_exceptions.YandexDiskAPIException(f"Failed to move {source_path} to {destination_path}.")

    async def copy(self, source_path: str, destination_path: str, overwrite: bool = False) -> None:
        """
            Copy a file or directory from one location to another on the disk.

            This method copies a file or directory from the source path to the destination path. If the request is successful (status code 202), it waits for the operation to finish and raises a YandexDiskAPIException if the operation fails. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response. If the auto_update_info attribute is True, it updates the disk information after the operation is successful.

            Parameters:
            - source_path (str): The path of the file or directory to be copied.
            - destination_path (str): The path where the file or directory should be copied to.
            - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails or if the operation fails.
            """
        response = await api_resources.copy(token=self.token, session=self.session, from_path=source_path,
                                            to_path=destination_path, force_async=True, overwrite=overwrite)

        response_json = await response.json()

        if response.status != 202:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        href = response_json.get("href", "")
        operation_id = href.split("/")[-1]
        operation_status = await self._wait_for_operation_to_finish(operation_id)

        if not operation_status:
            raise api_exceptions.YandexDiskAPIException(f"Failed to copy {source_path} to {destination_path}.")

        if self.auto_update_info:
            await self.update_disk_info()

    async def publish(self, path: str, return_public_url: bool = False) -> str | None:  # TODO: implement body
        """
            Publish a file or directory on the server.

            This method publishes a file or directory on the server using the provided path. If the request is successful (status code 200), it returns the public URL of the published file or directory. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str): The path of the file or directory to be published.
            - return_public_url (bool, optional): Whether to return the public URL of the published file or directory. Defaults to False.

            Returns:
            - str | None: The public URL of the published file or directory if return_public_url is True, otherwise None.

            Raises:
            - YandexDiskAPIException: If the request fails.
            """

        body = {
            "public_settings": {
                "read_only": False,
                "external_organization_id_verbose": {
                    "enabled": False,
                    "value": ""
                },
                "password_verbose": {
                    "enabled": False,
                    "value": ""
                },
                "available_until": False,
                "accesses": [
                    {}
                ],
                "available_until_verbose": {
                    "enabled": False,
                    "value": 0
                },
                "password": "",
                "external_organization_id": ""
            }
        }

        response = await api_resources.publish(token=self.token, session=self.session, path=path, body=body)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        if return_public_url:
            obj: File | Directory = await self.get_object(path)
            return obj.public_url

    async def unpublish(self, path: str):
        """
            Unpublish a file or directory on the server.

            This method unpublishes a file or directory on the server using the provided path. If the request is successful (status code 200), it returns the public URL of the unpublished file or directory. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str): The path of the file or directory to be unpublished.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails.
            """
        response = await api_resources.unpublish(token=self.token, session=self.session, path=path)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

    async def upload_file(self, file_path: str, path: str, overwrite: bool = False, chunk_size: int = 1024) -> None:
        """
            Upload a file to the server.

            This method uploads a file to the server using the provided file path and destination path. If the file size is larger than the available space or the maximum file size allowed, it raises a YandexDiskAPIException. If the request is successful (status code 201), it updates the disk information if auto_update_info is True. If the request is successful (status code 202), it waits for the operation to finish and updates the disk information if auto_update_info is True. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - file_path (str): The path of the file to be uploaded.
            - path (str): The destination path on the server.
            - overwrite (bool, optional): Whether to overwrite the destination file if it already exists. Defaults to False.
            - chunk_size (int, optional): The size of each chunk to be uploaded. Defaults to 1024.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the file size is too large or the request fails.
            """
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise ValueError(f"File {file_path} does not exist.")

        file_size = os.path.getsize(file_path)
        if file_size > (self.total_space - self.used_space):
            raise api_exceptions.YandexDiskAPIException(f"You don't have enough space to upload {file_size}.")
        elif file_size > self.max_file_size:
            raise api_exceptions.YandexDiskAPIException(f"File {file_path} is too large.")

        response = await api_resources.get_upload_url(token=self.token, session=self.session, path=path,
                                                      overwrite=overwrite)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        operation_id = response_json.get("operation_id", "")
        upload_url = response_json.get("href", "")

        async def chunked_file_reader(file_path_, chunk_size_):
            async with aiofiles.open(file_path_, "rb") as file_:
                while chunk := await file_.read(chunk_size_):
                    yield chunk

        upload_response = await self.session.put(url=upload_url, data=chunked_file_reader(file_path, chunk_size))

        upload_response_json = await upload_response.json()

        if upload_response.status != 202:
            raise api_exceptions.YandexDiskAPIException(upload_response.status,
                                                        upload_response_json.get("description", ""))

        if self.auto_update_info:
            await self.update_disk_info()

    async def get_url(self, path: str = "/") -> str:
        """
            Retrieve the URL for a specified path on the disk.

            This method fetches the URL corresponding to the provided path from the Yandex Disk. If the request is successful (status code 200), it returns the URL as a string. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str, optional): The path for which to retrieve the URL. Defaults to "/".

            Returns:
            - str: The URL associated with the specified path.

            Raises:
            - YandexDiskAPIException: If the request fails (status code other than 200).
            """
        response = await api_resources.get_url(token=self.token, session=self.session, path=path)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        return response_json.get("href", "")

    async def listdir_trash(self, path: str = "/", limit: int = 100, offset: int = 0) -> list[File | Directory]:
        """
            List the contents of a directory in the trash on the disk.

            This method retrieves the contents of a directory in the trash from the disk using the provided path. If the request is successful (status code 200), it returns a list of File or Directory objects representing the contents of the directory. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response.

            Parameters:
            - path (str, optional): The path of the directory in the trash to list. Defaults to "/".
            - limit (int, optional): The maximum number of items to return in the response. Defaults to 100.
            - offset (int, optional): The number of items to skip before returning the response. Defaults to 0.

            Returns:
            - list[File | Directory]: A list of File or Directory objects representing the contents of the directory in the trash.

            Raises:
            - YandexDiskAPIException: If the request fails or if the object type cannot be determined.
            """
        response = await api_trash_resources.get_info(token=self.token, session=self.session, path=path, limit=limit,
                                                      offset=offset)

        response_json = await response.json()

        if response.status != 200:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        embedded_items = response_json.get("_embedded", {}).get("items", [])
        directory_contents = []

        for item in embedded_items:
            item_type = item.get("type", "")
            if not item_type:
                continue

            match item_type:
                case "file":
                    directory_contents.append(
                        File(
                            token=self.token,
                            created_at=item.get("created", ""),
                            modified_at=item.get("modified", ""),
                            name=item.get("name", ""),
                            path=item.get("path", ""),
                            resource_id=item.get("resource_id", ""),
                            revision=item.get("revision", 0),
                            public_key=item.get("public_key", ""),
                            public_url=item.get("public_url", ""),
                            antivirus_status=item.get("antivirus_status", ""),
                            file_url=item.get("file", ""),
                            preview_url=item.get("preview", ""),
                            md5=item.get("md5", ""),
                            sha256=item.get("sha256", ""),
                            media_type=item.get("media_type", ""),
                            mime_type=item.get("mime_type", ""),
                            size=item.get("size", 0),
                            in_trash=True
                        )
                    )
                case "dir":
                    directory_contents.append(
                        Directory(
                            token=self.token,
                            created_at=item.get("created", ""),
                            modified_at=item.get("modified", ""),
                            name=item.get("name", ""),
                            path=item.get("path", ""),
                            resource_id=item.get("resource_id", ""),
                            revision=item.get("revision", 0),
                            public_key=item.get("public_key", ""),
                            public_url=item.get("public_url", ""),
                            in_trash=True
                        )
                    )
                case _:
                    continue

        return directory_contents

    async def delete_trash(self, path: str = ""):
        """
            Delete a file or directory from the trash on the server.

            This method deletes a file or directory from the trash using the provided path. If the request is successful (status code 202), it waits for the operation to finish and raises a YandexDiskAPIException if the operation fails. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response. If the auto_update_info attribute is True, it updates the disk information after the operation is successful.

            Parameters:
            - path (str, optional): The path of the file or directory to be deleted from the trash. Defaults to "".

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails or if the operation fails.
            """
        response = await api_trash_resources.delete(token=self.token, session=self.session, path=path, force_async=True)

        response_json = await response.json()

        if response.status != 202:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        href = response_json.get("href", "")
        operation_id = href.split("/")[-1]
        operation_status = await self._wait_for_operation_to_finish(operation_id)

        if not operation_status:
            raise api_exceptions.YandexDiskAPIException(f"Failed to delete {path}.")

        if self.auto_update_info:
            await self.update_disk_info()

    async def restore_trash(self, path: str, new_name: str = "", overwrite: bool = False):
        """
            Restore a file or directory from the trash on the server.

            This method restores a file or directory from the trash using the provided path. If the request is successful (status code 202), it waits for the operation to finish and raises a YandexDiskAPIException if the operation fails. If the request fails, it raises a YandexDiskAPIException with the status code and description from the response. If the auto_update_info attribute is True, it updates the disk information after the operation is successful.

            Parameters:
            - path (str): The path of the file or directory to be restored.
            - new_name (str, optional): The new name for the restored file or directory. Defaults to "".
            - overwrite (bool, optional): Whether to overwrite the destination file or directory if it already exists. Defaults to False.

            Returns:
            - None

            Raises:
            - YandexDiskAPIException: If the request fails or if the operation fails.
            """
        response = await api_trash_resources.restore(token=self.token, session=self.session, path=path, name=new_name,
                                                     overwrite=overwrite, force_async=True)

        response_json = await response.json()

        if response.status != 202:
            raise api_exceptions.YandexDiskAPIException(response.status, response_json.get("description", ""))

        href = response_json.get("href", "")
        operation_id = href.split("/")[-1]
        operation_status = await self._wait_for_operation_to_finish(operation_id)

        if not operation_status:
            raise api_exceptions.YandexDiskAPIException(f"Failed to restore {path}.")

        if self.auto_update_info:
            await self.update_disk_info()
