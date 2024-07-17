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
    __kwdefaults__: dict[str, str]
    __slots__: Final[tuple[str, ...]] = ()

    async def __call__(self, first: Interaction, *args: P.args, **kwargs: P.kwargs) -> R:
        ...


CommandFunc = CallabackProtocol[Any, CommandResponse]
