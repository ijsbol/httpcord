
from typing import Any, Final

from aiohttp import ClientSession
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
        json: dict[str, Any] | CommandDict | None = None,
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

    async def post(self, route: Route) -> dict[str, Any]:
        route.headers.update(self._headers)
        resp = await self._session.post(
            url=route.url,
            json=route.json,
            headers=route.headers,
        )
        return await resp.json()
