"""
MIT License

Copyright (c) 20234 Isabelle Phoebe <izzy@uwu.gal>

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

from dateutil.parser import parse
from fastapi import Request

from httpcord.enums import InteractionResponseType


__all__: Final[tuple[str, ...]] = (
    "Interaction",
)


class User:
    __slots__: Final[tuple[str, ...]] = (
        "id",
        "username",
        "role_ids",
        "joined_at",
        "nick",
        "display_name",
        "discriminator",
    )

    def __init__(
        self,
        id: int,
        username: str,
        role_ids: list[int],
        joined_at: datetime.datetime,
        nick: str,
        display_name: str,
        discriminator: int,
    ) -> None:
        self.id: int = id
        self.username: str = username
        self.role_ids: list[int] = role_ids
        self.joined_at: datetime.datetime = joined_at
        self.nick: str = nick
        self.display_name: str = display_name
        self.discriminator: int = discriminator

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"


class Interaction:
    __slots__: Final[tuple[str, ...]] = (
        "_data",
        "user",
    )

    def __init__(
        self,
        request: Request,
        data: dict[str, Any],
    ) -> None:
        self._data = data
        self.user = User(
            id=int(data["member"]["user"]["id"]),
            username=data["member"]["user"]["username"],
            role_ids=[int(_id) for _id in data["member"]["roles"]],
            joined_at=parse(data["member"]["joined_at"]),
            nick=data["member"]["nick"],
            display_name=data["member"]["user"]["global_name"],
            discriminator=int(data["member"]["user"]["discriminator"]),
        )


class CommandResponse:
    __slots__: Final[tuple[str, ...]] = (
        "type",
        "content",
    )

    def __init__(self, type: InteractionResponseType, *, content: str) -> None:
        self.type = type
        self.content = content

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "data": {
                "content": self.content,
            },
        }
