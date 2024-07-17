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
