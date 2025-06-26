import datetime
from typing import Final, TypedDict, NotRequired

from httpcord.asset import Asset


__all__: tuple[str, ...] = (
    "AvatarDecoration",
    "NUMBER_OF_DEFAULT_AVATARS",
)


NUMBER_OF_DEFAULT_AVATARS: Final[int] = 6


class AvatarDecorationData(TypedDict):
    code: NotRequired[str]
    expires_at: str | None
    id: str | None


class AvatarDecoration:
    __slots__: tuple[str, ...] = ("_data",)

    def __init__(self, data: AvatarDecorationData) -> None:
        self._data = data

    @property
    def asset(self) -> Asset | None:
        """The avatar decoration asset."""
        if "code" not in self._data:
            return None
        return Asset(f"https://cdn.discordapp.com/avatar-decoration-presets", self._data["code"])

    @property
    def expires_at(self) -> datetime.datetime | None:
        """The expiration date of the avatar decoration."""
        if self._data["expires_at"] is None:
            return None
        return datetime.datetime.fromtimestamp(int(self._data["expires_at"]), tz=datetime.timezone.utc)

    @property
    def id(self) -> str | None:
        """The ID of the avatar decoration."""
        return self._data.get("id")
