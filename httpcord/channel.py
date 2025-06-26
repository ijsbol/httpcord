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

from __future__ import annotations

import datetime
from enum import IntEnum
from typing import Any, Literal, Union

from httpcord.asset import Asset
from httpcord.user import User
from httpcord.utils.functions import from_timestamp


__all__: tuple[str, ...] = (
    "Channel",
    "BaseChannel",
    "GuildChannel",
    "DMChannel",
    "GroupDMChannel",
    "ChannelType",
)


class ChannelType(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16


class BaseChannel:
    __slots__: tuple[str, ...] = (
        "_data",
        "_id",
        "_flags",
        "_type",
        "_last_message_id",
        "_last_pin_timestamp",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self._id: int = int(data["id"])
        self._flags: int = data.get("flags", 0)
        self._type: int = int(data["type"])
        self._last_message_id: int | None = int(data["last_message_id"]) if data.get("last_message_id") else None
        self._last_pin_timestamp: str | None = data.get("last_pin_timestamp")

    @property
    def id(self) -> int:
        """The channel ID."""
        return self._id

    @property
    def flags(self) -> int:
        """The channel flags."""
        return self._flags

    @property
    def type(self) -> ChannelType:
        """The channel type."""
        return ChannelType(self._type)

    @property
    def last_message_id(self) -> int | None:
        """The ID of the last message sent in the channel."""
        return self._last_message_id

    @property
    def last_pin_timestamp(self) -> datetime.datetime | None:
        """The timestamp of the last pinned message in the channel."""
        return from_timestamp(self._last_pin_timestamp) if self._last_pin_timestamp else None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> BaseChannel:
        """Create a channel instance from raw data."""
        channel_type = ChannelType(data["type"])
        if channel_type == ChannelType.DM:
            return DMChannel(data)
        elif channel_type == ChannelType.GROUP_DM:
            return GroupDMChannel(data)
        elif channel_type in (ChannelType.GUILD_TEXT, ChannelType.GUILD_VOICE, ChannelType.GUILD_CATEGORY):
            return GuildChannel(data)
        else:
            return BaseChannel(data)


class GuildChannel(BaseChannel):
    __slots__: tuple[str, ...] = (
        "_name",
        "_topic",
        "_nsfw",
        "_rate_limit_per_user",
        "_guild_id",
        "_position",
        "_permission_overwrites",
        "_default_auto_archive_duration",
        "_parent_id",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(data)
        self._name: str = data["name"]
        self._topic: str | None = data.get("topic")
        self._nsfw: bool = data.get("nsfw", False)
        self._rate_limit_per_user: int | None = data.get("rate_limit_per_user", None)
        self._guild_id: int = int(data["guild_id"])
        self._position: int = data.get("position", 0)
        self._permission_overwrites: list[dict[str, Any]] = data.get("permission_overwrites", [])
        self._default_auto_archive_duration: int | None = data.get("default_auto_archive_duration", None)

    @property
    def name(self) -> str:
        """The channel name."""
        return self._name

    @property
    def topic(self) -> str | None:
        """The channel topic."""
        return self._topic

    @property
    def nsfw(self) -> bool:
        """Whether the channel is marked as NSFW."""
        return self._nsfw

    @property
    def rate_limit_per_user(self) -> int | None:
        """The rate limit per user in seconds."""
        return self._rate_limit_per_user

    @property
    def guild_id(self) -> int:
        """The ID of the guild this channel belongs to."""
        return self._guild_id

    @property
    def position(self) -> int:
        """The position of the channel in the guild's channel list."""
        return self._position

    @property
    def permission_overwrites(self) -> list[dict[str, Any]]:
        """The permission overwrites for the channel."""
        return self._permission_overwrites

    @property
    def default_auto_archive_duration(self) -> int | None:
        """The default auto archive duration for the channel."""
        return self._default_auto_archive_duration

    @property
    def parent_id(self) -> int | None:
        """The ID of the parent category channel, if any."""
        return self._parent_id


class DMChannel(BaseChannel):
    __slots__: tuple[str, ...] = ("_recipients",)

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(data)
        self._recipients: list[dict[str, Any]] = data.get("recipients", [])

    @property
    def type(self) -> Literal[ChannelType.DM]:
        """The channel type."""
        return ChannelType.DM

    @property
    def recipients(self) -> list[User]:
        """The IDs of the users in the DM channel."""
        return [User(recipient) for recipient in self._recipients]


class GroupDMChannel(DMChannel):
    __slots__: tuple[str, ...] = (
        "_name",
        "_icon",
        "_owner_id",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(data)
        self._name: str = data["name"]
        self._icon: str | None = data.get("icon")
        self._owner_id: int = int(data["owner_id"])

    @property
    def type(self) -> Literal[ChannelType.GROUP_DM]:  # pyright: ignore[reportIncompatibleMethodOverride]
        """The channel type."""
        return ChannelType.GROUP_DM

    @property
    def name(self) -> str:
        """The name of the group DM channel."""
        return self._name

    @property
    def icon(self) -> Asset | None:
        """The icon of the group DM channel."""
        return (
            Asset(
                base_url=f"https://cdn.discordapp.com/channel-icons/{self.id}",
                code=self._icon,
            )
            if self._icon
            else None
        )

    @property
    def owner_id(self) -> int:
        """The ID of the user who owns the group DM channel."""
        return self._owner_id


Channel = Union[
    BaseChannel,
    GuildChannel,
    DMChannel,
    GroupDMChannel,
]
