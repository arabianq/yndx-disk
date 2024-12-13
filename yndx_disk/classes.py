from dataclasses import dataclass, field


@dataclass
class BaseObject:
    token: str

    created_at: str
    modified_at: str

    name: str
    path: str

    resource_id: str

    revision: int

    public_key: str = ""
    public_url: str = ""

    in_trash: bool = False


@dataclass
class File(BaseObject):
    antivirus_status: str = ""
    file_url: str = ""
    preview_url: str = ""
    md5: str = ""
    sha256: str = ""
    media_type: str = ""
    mime_type: str = ""

    size: int = 0


@dataclass
class Directory(BaseObject):
    @property
    async def size(self) -> int:
        return 0

    @property
    async def contents(self) -> list:
        return []