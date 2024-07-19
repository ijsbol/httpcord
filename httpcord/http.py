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

from typing import TYPE_CHECKING, Any, Final, Literal, Union, overload

from aiohttp import ClientSession

if TYPE_CHECKING:
    from httpcord.command import CommandDict


class Route:
    DISCORD_API_BASE: Final[str] = "https://discord.com/api/v10"

    __slots__: Final[tuple[str, ...]] = (
        "url",
        "headers",
        "json",
    )

    def __init__(
        self,
        url: str,
        *,
        headers: dict[str, Any] | None = None,
        json: Union[dict[str, Any], "CommandDict", None] = None,
    ) -> None:
        self.url = Route.DISCORD_API_BASE + url
        self.headers = headers or {}
        self.json = json


class HTTP:
    __slots__: Final[tuple[str, ...]] = (
        "_token",
        "_session",
        "_headers",
    )

    def __init__(self, token: str) -> None:
        self._token = token
        self._session = ClientSession()
        self._headers: dict[str, str] = {
            "Authorization": f"Bot {self._token}",
            "Content-Type": "application/json",
            "User-Agent": "HTTPCord / Python - https://git.uwu.gal/pyhttpcord",
        }

    @overload
    async def post(self, route: Route, expect_return: Literal[True] = True) -> dict[str, Any]:
        ...

    @overload
    async def post(self, route: Route, expect_return: Literal[False] = False) -> None:
        ...

    async def post(self, route: Route, expect_return: bool = True) -> dict[str, Any] | None:
        route.headers.update(self._headers)
        resp = await self._session.post(
            url=route.url,
            json=route.json,
            headers=route.headers,
        )
        if expect_return:
            return await resp.json()
