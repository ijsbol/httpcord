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

from typing import Final, TypedDict

from httpcord.func_protocol import CommandFunc
from httpcord.interaction import CommandResponse, Interaction


__all__: Final[tuple[str, ...]] = (
    "Command",
)


class CommandOptionsDict(TypedDict):
    name: str
    description: str
    type: int  # TODO: types
    required: bool


class CommandDict(TypedDict):
    name: str
    type: int  # TODO: types
    intergration_types: list[int]  # TODO: types
    contexts: list[int]  # TODO: types
    description: str
    options: list[CommandOptionsDict]


class Command:
    __slots__: Final[tuple[str, ...]] = (
        "_func",
        "_name",
        "_description",
    )

    def __init__(
        self,
        func: CommandFunc,
        *,
        name: str,
        description: str | None = None,
    ) -> None:
        self._func: CommandFunc = func
        self._name: str = name
        self._description: str = description or "--"

    async def invoke(self, interaction: Interaction) -> CommandResponse:
        return await self._func(interaction)

    def creation_dict(self) -> CommandDict:
        return CommandDict(
            name=self._name,
            type=1,
            intergration_types=[0, 1],
            contexts=[0, 1, 2],
            description=self._description,
            options=[],
        )
