# yndx-disk

A modern, object-oriented Python wrapper for the Yandex.Disk REST API, featuring both synchronous and asynchronous
clients.

`yndx-disk` provides a clean and intuitive interface for managing your Yandex.Disk files, directories, public resources,
and trash. The library is built on `aiohttp` and `aiofiles`, ensuring efficient asynchronous operations, and provides a
synchronous client for simpler, blocking use cases.

## Features

- **Dual Clients**: Use the `AsyncDiskClient` for modern `asyncio` applications or the simple `DiskClient` for
  synchronous scripts.
- **Object-Oriented**: Interact with `File` and `Directory` objects that hold resource metadata.
- **Full API Coverage**: Manage files and directories (list, upload, download, move, copy, delete).
- **Trash Management**: List, restore, or permanently delete items from the trash.
- **Public Resources**: Publish files and directories to create public links.
- **Type Hinting**: Fully type-hinted codebase for better autocompletion and static analysis.

## Installation

Install the library using pip:

```sh
pip install yndx-disk
```

## Getting Started

First, you need to obtain a Yandex.Disk OAuth token. You can get one for development purposes from
the [Yandex.Disk Polygon](https://yandex.ru/dev/disk/poligon/).

### Synchronous Client Example

The `DiskClient` provides a straightforward, blocking interface.

```python
from yndx_disk.clients import DiskClient

# You must provide your OAuth token
TOKEN = "YOUR_OAUTH_TOKEN_HERE"

if TOKEN == "YOUR_OAUTH_TOKEN_HERE":
    print("Please provide your Yandex.Disk OAuth token.")
else:
    # 1. Initialize the client
    client = DiskClient(token=TOKEN)

    # 2. Get and print basic disk information
    client.update_disk_info()
    print(f"Total Space: {client.total_space // 1024 ** 3} GB")
    print(f"Used Space: {client.used_space // 1024 ** 3} GB")

    # 3. Create a dummy file to upload
    with open("hello.txt", "w") as f:
        f.write("Hello, Yandex.Disk!")

    # 4. Upload the file to the root of the disk
    try:
        print("\nUploading 'hello.txt'...")
        client.upload_file("hello.txt", "/hello.txt", overwrite=True)
        print("Upload successful.")
    except Exception as e:
        print(f"Upload failed: {e}")

    # 5. List files in the root directory
    print("\nListing files in '/':")
    items = client.listdir("/")
    for item in items:
        item_type = "d" if "Directory" in str(type(item)) else "f"
        print(f"[{item_type}] {item.path}")

    # 6. Delete the file from the disk
    try:
        print("\nDeleting '/hello.txt'...")
        client.delete("/hello.txt")
        print("Deletion successful.")
    except Exception as e:
        print(f"Deletion failed: {e}")
```

### Asynchronous Client Example

The `AsyncDiskClient` is perfect for non-blocking I/O operations in `asyncio`-based applications.

```python
import asyncio
from yndx_disk.clients import AsyncDiskClient

# You must provide your OAuth token
TOKEN = "YOUR_OAUTH_TOKEN_HERE"


async def main():
    if TOKEN == "YOUR_OAUTH_TOKEN_HERE":
        print("Please provide your Yandex.Disk OAuth token.")
        return

    # 1. Initialize the async client
    client = AsyncDiskClient(token=TOKEN)

    # 2. Get and print basic disk information
    await client.update_disk_info()
    print(f"Total Space: {client.total_space // 1024 ** 3} GB")
    print(f"Used Space: {client.used_space // 1024 ** 3} GB")

    # 3. Create a dummy file to upload
    with open("hello_async.txt", "w") as f:
        f.write("Hello, Async Yandex.Disk!")

    # 4. Upload the file to the root of the disk
    try:
        print("\nUploading 'hello_async.txt'...")
        await client.upload_file("hello_async.txt", "/hello_async.txt", overwrite=True)
        print("Upload successful.")
    except Exception as e:
        print(f"Upload failed: {e}")

    # 5. List files in the root directory
    print("\nListing files in '/':")
    items = await client.listdir("/")
    for item in items:
        item_type = "d" if "Directory" in str(type(item)) else "f"
        print(f"[{item_type}] {item.path}")

    # 6. Delete the file from the disk
    try:
        print("\nDeleting '/hello_async.txt'...")
        await client.delete("/hello_async.txt")
        print("Deletion successful.")
    except Exception as e:
        print(f"Deletion failed: {e}")

    # Remember to close the session when you're done
    await client.session.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## API Overview

Both `DiskClient` and `AsyncDiskClient` share the same methods. For the async client, all methods are coroutines and
must be awaited.

### Disk and Resource Management

| Method                                    | Description                                                     |
|-------------------------------------------|-----------------------------------------------------------------|
| `update_disk_info()`                      | Refreshes disk info (space, user, etc.) on the client instance. |
| `get_object(path)`                        | Retrieves a `File` or `Directory` object for the given path.    |
| `listdir(path, limit, offset)`            | Lists the contents of a directory.                              |
| `upload_file(file_path, path, overwrite)` | Uploads a local file to the specified path on the disk.         |
| `get_url(path)`                           | Gets a download URL for a file or folder.                       |
| `delete(path, permanently)`               | Deletes a file or folder (moves to trash by default).           |
| `copy(source_path, destination_path)`     | Copies a file or folder.                                        |
| `move(source_path, destination_path)`     | Moves a file or folder.                                         |
| `publish(path)`                           | Makes a resource public and returns its public URL.             |
| `unpublish(path)`                         | Reverts a public resource to private.                           |

### Trash Management

| Method                               | Description                                                                              |
|--------------------------------------|------------------------------------------------------------------------------------------|
| `listdir_trash(path, limit, offset)` | Lists items in the trash.                                                                |
| `restore_trash(path, new_name)`      | Restores a file or folder from the trash, optionally renaming it.                        |
| `delete_trash(path)`                 | Permanently deletes an item from the trash. If `path` is empty, clears the entire trash. |

## License

This project is licensed under the MIT License.