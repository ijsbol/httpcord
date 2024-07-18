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

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Final

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
import uvicorn

from httpcord.command import Command
from httpcord.enums import InteractionResponseType, InteractionType
from httpcord.errors import UnknownCommand
from httpcord.func_protocol import CommandFunc
from httpcord.http import HTTP, Route
from httpcord.interaction import Interaction

from .types import JSONResponseError, JsonResponseType


__all__: Final[tuple[str, ...]] = (
    "HTTPBot",
)


DEFAULT_FASTAPI_KWARGS: Final[dict[str, Any]] = {
    "debug": False,
    "title": "Discord HTTPBot - Python FastAPI https://git.uwu.gal/pyhttpcord",
    "openapi_url": None,
    "docs_url": None,
    "redoc_url": None,
    "swagger_ui_init_oauth": None,
    "include_in_schema": False,
}

ERROR_BAD_SIGNATURE_REQUEST: Final[JSONResponse] = JSONResponse(
    status_code=HTTPStatus.UNAUTHORIZED,
    content=JSONResponseError(
        error="Bad request signature",
    ),
)


class HTTPBot:
    __slots__: Final[tuple[str, ...]] = (
        "http",
        "_token",
        "_id",
        "_public_key",
        "_register_commands_on_startup",
        "_fastapi",
        "_commands",
        "_uri_path",
    )

    def __init__(
        self,
        *,
        client_id: int,
        client_public_key: str,
        register_commands_on_startup: bool = False,
        uri_path: str = "/api/interactions",
        **kwargs: Any,
    ) -> None:
        """ Create an HTTPBot client. """
        self.http: HTTP
        self._token: str
        self._id: Final[int] = client_id
        self._public_key: Final[str] = client_public_key
        self._register_commands_on_startup = register_commands_on_startup
        self._fastapi = FastAPI(
            **DEFAULT_FASTAPI_KWARGS,
            **kwargs,
            on_startup=[self._setup],
        )
        self._commands: dict[str, Command] = {}
        self._uri_path: str = uri_path
        self._fastapi.add_api_route(
            path=self._uri_path,
            endpoint=self._interaction_http_callback,
            name="HTTP Interaction Bot entry point",
            methods=["POST"],
        )

    def command(self, name: str, *, description: str | None = None):
        def _decorator(func):
            self._commands[name] = Command(
                func=func,
                name=name,
                description=description,
            )
        return _decorator

    def __process_data(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplemented()

    def _register_command(
        self,
        func: CommandFunc,
        *,
        name: str,
        description: str | None = None,
    ) -> Command:
        command = Command(func, name=name, description=description)
        self._commands[name] = command
        return command

    async def _verify_signature(self, request: Request) -> bool:
        signature: str | None = request.headers.get('X-Signature-Ed25519')
        timestamp: str | None = request.headers.get('X-Signature-Timestamp')
        if (
            signature is None
            or timestamp is None
        ):
            return False
        else:
            message = timestamp.encode() + await request.body()
            try:
                vk = VerifyKey(bytes.fromhex(self._public_key))
                vk.verify(message, bytes.fromhex(signature))
            except Exception:
                return False
        return True

    async def _handle_verified_interaction(self, request: Request) -> JSONResponse:
        request_json = await request.json()
        if request_json['type'] == InteractionType.PING:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=JsonResponseType(
                    type=InteractionResponseType.PONG,
                ),
            )
        return await self.__process_commands(request, request_json)

    async def ___create_interaction(self, request: Request, data: dict[str, Any]) -> Interaction:
        return Interaction(request, data)

    async def __process_commands(self, request: Request, data: dict[str, Any]) -> JSONResponse:
        command_name = data.get("data", {}).get("name", None)
        command = self._commands.get(command_name, None)
        if command:
            interaction = await self.___create_interaction(request, data)
            options = {arg['name']: arg['value'] for arg in data["data"].get("options", [])}
            response = await command.invoke(interaction, **options)
            return JSONResponse(content=response.to_dict())
        raise UnknownCommand(f"Unknown command used: {command}")

    async def _interaction_http_callback(self, request: Request) -> JSONResponse:
        verified_signature = await self._verify_signature(request)
        if not verified_signature:
            return ERROR_BAD_SIGNATURE_REQUEST

        return await self._handle_verified_interaction(request)

    async def register_commands(self) -> None:
        for _, command in self._commands.items():
            await self.http.post(Route(
                f"/applications/{self._id}/commands",
                json=command.creation_dict(),
            ))

    async def _setup(self) -> None:
        self.http = HTTP(token=self._token)
        if self._register_commands_on_startup:
            await self.register_commands()

    def start(self, token: str, **kwargs: Any) -> None:
        self._token = token
        uvicorn.run(app=self._fastapi, **kwargs)
