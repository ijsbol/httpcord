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

from dataclasses import dataclass
from typing import Final, TypedDict

from httpcord.attachment import Attachment
from httpcord.channel import BaseChannel
from httpcord.enums import (
    ApplicationCommandOptionType,
    InteractionResponseType,
)
from httpcord.member import Member
from httpcord.role import Role
from httpcord.user import User


__all__: Final[tuple[str, ...]] = (
    "JSON",
    "JSONResponseError",
    "JSONResponseType",
    "TYPE_CONVERSION_TABLE",
    "Integer",
    "Float",
    "String",
)


type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None


@dataclass(slots=True)
class Integer:
    """Dataclass for integer constraints, with validation to ensure min_value <= max_value if both are provided."""

    min_value: int | None = None
    max_value: int | None = None

    def __post_init__(self):
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValueError("min_value cannot be greater than max_value")


@dataclass(slots=True)
class Float:
    """Dataclass for float constraints, with validation to ensure min_value <= max_value if both are provided."""

    min_value: float | None = None
    max_value: float | None = None

    def __post_init__(self):
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValueError("min_value cannot be greater than max_value")


@dataclass(slots=True)
class String:
    """Dataclass for string constraints, with validation to ensure min_length <= max_length if both are provided."""

    min_length: int | None = None
    max_length: int | None = None

    def __post_init__(self):
        if self.min_length is not None and self.max_length is not None and self.min_length > self.max_length:
            raise ValueError("min_length cannot be greater than max_length")


"""Dictionary mapping Python types to Discord application command option types for consistent type handling."""
TYPE_CONVERSION_TABLE: dict[type, ApplicationCommandOptionType] = {
    bool: ApplicationCommandOptionType.BOOLEAN,
    int: ApplicationCommandOptionType.INTEGER,
    float: ApplicationCommandOptionType.NUMBER,
    str: ApplicationCommandOptionType.STRING,
    User: ApplicationCommandOptionType.USER,
    Member: ApplicationCommandOptionType.USER,
    Attachment: ApplicationCommandOptionType.ATTACHMENT,
    BaseChannel: ApplicationCommandOptionType.CHANNEL,
    # mentionable: ApplicationCommandOptionType.MENTIONABLE,
    Role: ApplicationCommandOptionType.ROLE,
}


class JSONResponseError(TypedDict):
    error: str


class JSONResponseType(TypedDict):
    type: InteractionResponseType
