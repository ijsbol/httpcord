from typing import (
    Any,
    Awaitable,
    Final,
    ParamSpec,
    Protocol,
    TypeVar,
)

from httpcord.interaction import CommandResponse, Interaction


__all__: Final[tuple[str, ...]] = (
    "CommandFunc",
)


P = ParamSpec('P')
R = TypeVar('R', covariant=True)


class CallabackProtocol(Protocol[P, R]):
    __slots__: Final[tuple[str, ...]] = ()

    async def __call__(self, first: Interaction, *args: P.args, **kwargs: P.kwargs) -> R:
        ...


CommandFunc = CallabackProtocol[Any, CommandResponse]
