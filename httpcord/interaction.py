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

from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    NotRequired,
    TypedDict,
)

from fastapi import Request

from httpcord.channel import BaseChannel, Channel
from httpcord.embed import Embed
from httpcord.enums import InteractionResponseFlags, InteractionResponseType
from httpcord.file import File
from httpcord.http import Route
from httpcord.member import Member
from httpcord.message import PartialMessage
from httpcord.role import Role
from httpcord.user import User


if TYPE_CHECKING:
    from httpcord.bot import HTTPBot


__all__: Final[tuple[str, ...]] = ("Interaction",)


class InteractionDeferData(TypedDict):
    type: int
    data: NotRequired[dict[str, int]]


class Resolved:
    __slots__: tuple[str, ...] = (
        "_users",
        "_members",
        "_channels",
        "_roles",
        "_messages",
    )

    def __init__(self, data: dict[str, Any]) -> None:
        resolved = data["data"].get("resolved", {})
        guild_id = int(data["guild_id"]) if "guild_id" in data else None
        self._users: dict[int, User] = {int(k): User(v) for k, v in resolved.get("users", {}).items()}
        for user_id in resolved.get("members", {}).keys():
            resolved["members"][str(user_id)]["user"] = resolved["users"][str(user_id)]
        self._members: dict[int, Member] = {
            int(k): Member(v, guild_id or 0) for k, v in resolved.get("members", {}).items()
        }
        self._channels: dict[int, Channel] = {
            int(k): BaseChannel.from_data(v) for k, v in resolved.get("channels", {}).items()
        }
        self._roles: dict[int, Role] = {int(k): Role(v) for k, v in resolved.get("roles", {}).items()}
        self._messages: dict[int, PartialMessage] = {
            int(k): PartialMessage(v) for k, v in resolved.get("messages", {}).items()
        }

    @property
    def users(self) -> dict[int, User]:
        """A dictionary of resolved users."""
        return self._users

    @property
    def members(self) -> dict[int, Member]:
        """A dictionary of resolved members."""
        return self._members

    @property
    def channels(self) -> dict[int, Channel]:
        """A dictionary of resolved channels."""
        return self._channels

    @property
    def roles(self) -> dict[int, Role]:
        """A dictionary of resolved roles."""
        return self._roles

    @property
    def messages(self) -> dict[int, PartialMessage]:
        """A dictionary of resolved messages."""
        return self._messages


class Interaction[HTTPBotClient: HTTPBot = HTTPBot]:
    __slots__: tuple[str, ...] = (
        "_data",
        "_id",
        "_member",
        "_user",
        "_deferred",
        "_responded",
        "_request",
        "_bot",
        "_token",
        "_channel",
        "_guild_id",
        "_resolved",
    )

    def __init__(
        self,
        request: Request,
        data: dict[str, Any],
        bot: HTTPBotClient,
    ) -> None:
        self._data: dict[str, Any] = data
        self._bot: HTTPBotClient = bot
        self._request: Request = request
        self._id = int(data["id"])
        self._token: str = data["token"]
        self._channel = data["channel"]
        self._guild_id: str | None = data.get("guild_id")
        if data.get("member", None) is not None:
            assert self._guild_id is not None, "Guild ID must be present if member data is provided."
            self._member = Member(data["member"], int(self._guild_id))
            self._user = User(data["member"]["user"])
        else:
            self._user = User(data["user"])

        self._deferred: bool = False
        self._responded: bool = False
        self._resolved: Resolved = Resolved(data)

    @property
    def id(self) -> int:
        """The interaction ID."""
        return int(self._id)

    @property
    def guild_id(self) -> int | None:
        """The ID of the guild the interaction was sent in, if applicable."""
        return int(self._guild_id) if self._guild_id is not None else None

    @property
    def user(self) -> User:
        """The user who initiated the interaction."""
        return self._user

    @property
    def member(self) -> Member | None:
        """The member who initiated the interaction, if applicable."""
        return self._member if hasattr(self, "_member") else None

    @property
    def channel(self) -> Channel:
        """The channel the interaction was sent in."""
        return BaseChannel.from_data(self._channel)

    @property
    def token(self) -> str:
        """The interaction token."""
        return self._token

    @property
    def bot(self) -> HTTPBotClient:
        """The bot instance."""
        return self._bot

    @property
    def deffered(self) -> bool:
        """Whether the interaction has been deferred."""
        return self._deferred

    @property
    def responded(self) -> bool:
        """Whether the interaction has been responded to."""
        return self._responded

    @property
    def resolved(self) -> Resolved:
        """The resolved data for the interaction."""
        return self._resolved

    async def defer(self, *, with_message: bool = True, ephemeral: bool = False) -> None:
        """Defers the interaction response."""
        if self._deferred or self._responded:
            raise RuntimeError("Interaction has already been deferred or responded to.")

        deferral_type: InteractionResponseType = (
            InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            if with_message
            else InteractionResponseType.DEFERRED_UPDATE_MESSAGE
        )
        self._deferred = True
        self._responded = True

        payload: InteractionDeferData = {
            "type": deferral_type.value,
        }
        if ephemeral:
            payload.update(
                {
                    "data": {
                        "flags": InteractionResponseFlags.EPHEMERAL.value,
                    },
                }
            )

        await self.bot.http.post(
            Route(
                f"/interactions/{self.id}/{self.token}/callback",
                json=payload,
            ),
            expect_return=False,
        )

    async def followup(self, response: CommandResponse) -> None:
        self._responded = True
        await self.bot.http.post(
            Route(
                f"/webhooks/{self.bot._id}/{self.token}",
                json=response.to_dict()["data"],
                files=response.files if response.files else None,
            ),
            expect_return=False,
        )


class CommandResponse:
    __slots__: Final[tuple[str, ...]] = (
        "_type",
        "_content",
        "_embeds",
        "_flags",
        "_files",
    )

    def __init__(
        self,
        type: InteractionResponseType,
        *,
        content: str | None = None,
        embeds: list[Embed] | None = None,
        ephemeral: bool = False,
        files: list[File] | None = None,
    ) -> None:
        self._type: InteractionResponseType = type
        self._content: str | None = content
        self._embeds: list[Embed] = embeds or []
        self._flags = InteractionResponseFlags.EPHEMERAL if ephemeral else None
        self._files: list[File] = files or []

    @property
    def files(self) -> list[File]:
        """The files in the response."""
        return self._files

    @property
    def type(self) -> InteractionResponseType:
        """The type of the response."""
        return self._type

    @property
    def content(self) -> str | None:
        """The content of the response."""
        return self._content

    @property
    def embeds(self) -> list[Embed]:
        """The embeds in the response."""
        return self._embeds

    @property
    def ephemeral(self) -> bool:
        """Whether the response is ephemeral."""
        return self._flags == InteractionResponseFlags.EPHEMERAL

    @property
    def flags(self) -> InteractionResponseFlags | None:
        """The flags of the response."""
        return self._flags

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "data": {
                "flags": self.flags,
                "content": self.content,
                "embeds": [e.to_dict() for e in self.embeds],
                "attachments": [
                    {
                        "id": idx,
                        "filename": file.filename,
                        "description": file.description,
                        "spoiler": file.spoiler,
                    }
                    for idx, file in enumerate(self.files)
                ],
            },
        }
