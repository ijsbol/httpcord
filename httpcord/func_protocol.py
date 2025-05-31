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

from typing import (
    Any,
    Callable,
    Coroutine,
    Final,
    List,
    ParamSpec,
    Protocol,
    TypeVar,
)

from httpcord.command.types import Choice
from httpcord.interaction import CommandResponse, Interaction


__all__: Final[tuple[str, ...]] = (
    "CommandFunc",
    "AutocompleteFunc",
)


P = ParamSpec('P')
R = TypeVar('R', covariant=True)


class CommandCallabackProtocol(Protocol[P, R]):
    '''Protocol for command callback functions, defining the signature for functions that handle interactions and return a CommandResponse.'''
    __kwdefaults__: dict[str, str]
    __slots__: Final[tuple[str, ...]] = ()

    async def __call__(self, interaction: Interaction, *args: P.args, **kwargs: P.kwargs) -> R:
        ...


class AutocompleteCallabackProtocol(Protocol[P, R]):
    '''Protocol for autocomplete callback functions, defining the signature for functions that handle autocomplete queries and return choices.'''
    __kwdefaults__: dict[str, str]
    __slots__: Final[tuple[str, ...]] = ()

    async def __call__(self, interaction: Interaction, current: str) -> R:
        ...


'''Type alias for command functions, representing asynchronous functions that take an interaction and return a CommandResponse.'''
CommandFunc = CommandCallabackProtocol[Any, CommandResponse]

'''Type alias for autocomplete functions, representing asynchronous functions that take an interaction and a string, returning a list of choices.'''
AutocompleteFunc = Callable[[Interaction, str], Coroutine[Any, Any, List[Choice]]]
