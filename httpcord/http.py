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

import json
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    Literal,
    overload,
)

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from httpcord.file import File
from httpcord.types import JSON


class Route:
    DISCORD_API_BASE: Final[str] = "https://discord.com/api/v10"

    __slots__: Final[tuple[str, ...]] = (
        "_url",
        "_headers",
        "_json",
        "_files",
    )

    def __init__(
        self,
        url: str,
        *,
        headers: dict[str, Any] | None = None,
        json: Any | None = None,
        files: list[File] | None = None,
    ) -> None:
        self._url = url
        self._headers = headers or {}
        self._json = json
        self._files = files or []

    @property
    def content_type(self) -> str:
        """The content type of the route."""
        if self.json is not None:
            return "application/json"
        return "multipart/form-data"

    @property
    def url(self) -> str:
        """The URL of the route."""
        return Route.DISCORD_API_BASE + self._url

    @property
    def headers(self) -> dict[str, Any]:
        """The headers of the route."""
        _headers = self._headers.copy()

        # FIX: I have no idea why, but whenever we send a multipart/form-data request,
        # Discord ignores the payload_json key in form data.
        # _headers["Content-Type"] = self.content_type
        return _headers

    @property
    def json(self) -> JSON:
        """The JSON data to send with the route."""
        if self._json is None or len(self._files) > 0:
            return None
        return self._json

    @property
    def data(self) -> dict[str, str | bytes] | None:
        """The data to send with the route."""

        if len(self._files) == 0:
            return None

        data: dict[str, str | bytes] = {}
        for idx, file in enumerate(self._files):
            data[f"files[{idx}]"] = file.read()

        if self._json is not None:
            data["payload_json"] = json.dumps(self._json)

        return data


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
            "User-Agent": "HTTPCord / Python - https://git.uwu.gal/pyhttpcord",
        }

    if TYPE_CHECKING:

        @overload
        async def post(self, route: Route, expect_return: Literal[True] = ...) -> dict[str, Any]: ...

        @overload
        async def post(self, route: Route, expect_return: Literal[False] = ...) -> None: ...

        @overload
        async def put(self, route: Route, expect_return: Literal[True] = ...) -> dict[str, Any]: ...

        @overload
        async def put(self, route: Route, expect_return: Literal[False] = ...) -> None: ...

        @overload
        async def patch(self, route: Route, expect_return: Literal[True] = ...) -> dict[str, Any]: ...

        @overload
        async def patch(self, route: Route, expect_return: Literal[False] = ...) -> None: ...

    async def post(self, route: Route, expect_return: bool = True) -> dict[str, Any] | None:
        try:
            headers = self._headers
            headers.update(route.headers)
            resp = await self._session.post(
                url=route.url,
                json=route.json,
                data=route.data,
                headers=headers,
            )
            if expect_return:
                json = await resp.json()
                logging.getLogger("httpcord").debug(f"POST {route.url} returned {json}")
                return json

            if logging.getLogger("httpcord").isEnabledFor(logging.DEBUG):
                logging.getLogger("httpcord").debug(f"POST {route.url} returned {await resp.json()}")
        except ClientError as e:
            raise RuntimeError(f"POST request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in POST: {e}")

    async def put(self, route: Route, expect_return: bool = True) -> dict[str, Any] | None:
        try:
            headers = self._headers
            headers.update(route.headers)
            resp = await self._session.put(
                url=route.url,
                json=route.json,
                data=route.data,
                headers=headers,
            )
            if expect_return:
                json = await resp.json()
                logging.getLogger("httpcord").debug(f"PUT {route.url} returned {json}")
                return json

            if logging.getLogger("httpcord").isEnabledFor(logging.DEBUG):
                logging.getLogger("httpcord").debug(f"PUT {route.url} returned {await resp.json()}")
        except ClientError as e:
            raise RuntimeError(f"PUT request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in PUT: {e}")

    async def patch(self, route: Route, expect_return: bool = True) -> dict[str, Any] | None:
        try:
            headers = self._headers
            headers.update(route.headers)
            resp = await self._session.patch(
                url=route.url,
                json=route.json,
                data=route.data,
                headers=headers,
            )
            if expect_return:
                json = await resp.json()
                logging.getLogger("httpcord").debug(f"PATCH {route.url} returned {json}")
                return json

            if logging.getLogger("httpcord").isEnabledFor(logging.DEBUG):
                logging.getLogger("httpcord").debug(f"PATCH {route.url} returned {await resp.json()}")
        except ClientError as e:
            raise RuntimeError(f"PATCH request failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error in PATCH: {e}")
