"""
MIT License

Copyright (c) 2024-present Isabelle Phoebe <izzy@uwu.gal>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
from typing import Any, Final

from httpcord.asset import Asset
from httpcord.avatar import NUMBER_OF_DEFAULT_AVATARS, AvatarDecoration, AvatarDecorationData


__all__: tuple[str, ...] = ("User",)


class Nameplate:
    __slots__: Final[tuple[str, ...]] = (
        "_expires_at",
        "_asset",
        "_pallet",
        "_label",
        "_sku_id",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        self._expires_at: datetime.datetime | None = (
            datetime.datetime.fromtimestamp(int(data["expires_at"]), tz=datetime.timezone.utc)
            if data["expires_at"] is not None
            else None
        )
        self._asset = data["asset"]
        self._pallet: str = data["pallet"]
        self._label: str = data["label"]
        self._sku_id: int = int(data["sku_id"])

    @property
    def asset(self) -> Asset | None:
        """The nameplate asset URL."""
        return Asset(
            f"https://cdn.discordapp.com/assets/collectibles/{self._asset}/",
            code=self._pallet,
        )

    @property
    def expires_at(self) -> datetime.datetime | None:
        """The expiration date of the nameplate."""
        return self._expires_at

    @property
    def label(self) -> str:
        """The label of the nameplate."""
        return self._label

    @property
    def pallet(self) -> str:
        """The color palette of the nameplate."""
        return self._pallet

    @property
    def sku_id(self) -> int:
        """The SKU ID of the nameplate."""
        return self._sku_id


class Collectibles:
    __slots__: Final[tuple[str, ...]] = ("_nameplate",)

    def __init__(self, collectibles: dict[str, Any] | None) -> None:
        self._nameplate = Nameplate(collectibles["nameplate"]) if collectibles and "nameplate" in collectibles else None

    @property
    def nameplate(self) -> Nameplate | None:
        """The user's nameplate."""
        return self._nameplate


class PrimaryGuild:
    __slots__: Final[tuple[str, ...]] = (
        "_badge",
        "_identity_enabled",
        "_identity_guild_id",
        "_tag",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        self._badge: str | None = data.get("badge")
        self._identity_enabled: bool = data.get("identity_enabled", False)
        self._identity_guild_id: int | None = int(data["identity_guild_id"]) if "identity_guild_id" in data else None
        self._tag: str | None = data.get("tag")

    @property
    def identity_enabled(self) -> bool:
        """The ID of the primary guild."""
        return self._identity_enabled

    @property
    def identity_guild_id(self) -> int | None:
        """The name of the primary guild."""
        return self._identity_guild_id

    @property
    def tag(self) -> str | None:
        """The tag of the primary guild."""
        return self._tag

    @property
    def badge(self) -> Asset | None:
        """The badge of the primary guild."""
        if self._badge is None:
            return None
        if self.identity_guild_id is None:
            return None
        return Asset(
            f"https://cdn.discordapp.com/clan-badges/{self.identity_guild_id}/",
            self._badge,
        )


class User:
    __slots__: Final[tuple[str, ...]] = (
        "_id",
        "_username",
        "_avatar",
        "_avatar_decoration",
        "_primary_guild",
        "_collectibles",
        "_global_name",
        "_public_flags",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        self._id: int = int(data["id"])
        self._avatar: str | None = data.get("avatar")
        self._avatar_decoration: dict[str, Any] | None = data.get("avatar_decoration_data")
        self._primary_guild: dict[str, Any] | None = data.get("primary_guild")
        self._collectibles: dict[str, dict[str, Any]] | None = data.get("collectibles")
        self._global_name: str | None = data.get("global_name")
        self._public_flags: int = data.get("public_flags", 0)
        self._username: str = data["username"]

    @property
    def id(self) -> int:
        return self._id

    @property
    def avatar(self) -> Asset:
        """The user's avatar."""
        if self._avatar is None:
            return self.default_avatar
        return Asset(
            base_url=f"https://cdn.discordapp.com/avatars/{self.id}",
            code=self._avatar,
        )

    @property
    def default_avatar(self) -> Asset:
        """The default avatar icon."""
        avatar_id = (self.id >> 22) % NUMBER_OF_DEFAULT_AVATARS
        return Asset(f"https://cdn.discordapp.com/embed/avatars", str(avatar_id))

    @property
    def avatar_decoration(self) -> AvatarDecoration | None:
        """The avatar decoration."""
        if self._avatar_decoration is None:
            return None
        return AvatarDecoration(AvatarDecorationData(**self._avatar_decoration))

    @property
    def primary_guild(self) -> PrimaryGuild | None:
        """The user's primary guild."""
        return PrimaryGuild(self._primary_guild) if self._primary_guild else None

    @property
    def collectibles(self) -> Collectibles:
        """The user's collectibles."""
        return Collectibles(self._collectibles)

    @property
    def global_name(self) -> str | None:
        """The user's global name."""
        return self._global_name

    @property
    def public_flags(self) -> int:
        """The user's public flags."""
        return self._public_flags

    @property
    def username(self) -> str:
        """The user's username."""
        return self._username

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"
