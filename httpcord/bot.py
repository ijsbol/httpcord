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

import enum
from http import HTTPStatus
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Final,
    Literal,
    overload,
)

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey

from httpcord.attachment import Attachment
from httpcord.command import (
    AutocompleteResponse,
    Command,
    CommandData,
)
from httpcord.command.base import InteractionContextType
from httpcord.command.types import ApplicationCommandOptionType
from httpcord.enums import (
    ApplicationCommandType,
    ApplicationIntegrationType,
    InteractionResponseType,
    InteractionType,
)
from httpcord.errors import UnknownCommand
from httpcord.func_protocol import AutocompleteFunc
from httpcord.http import HTTP, Route
from httpcord.interaction import CommandResponse, Interaction
from httpcord.locale import Locale, LocaleDict
from httpcord.member import Member
from httpcord.types import JSONResponseError, JSONResponseType
from httpcord.user import User


__all__: Final[tuple[str, ...]] = ("HTTPBot",)


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
        "_on_startup",
        "_on_shutdown",
    )

    def __init__(
        self,
        *,
        client_id: int,
        client_public_key: str,
        register_commands_on_startup: bool = False,
        uri_path: str = "/api/interactions",
        on_startup: Callable[[], Coroutine[Any, Any, None]] | None = None,
        on_shutdown: Callable[[], Coroutine[Any, Any, None]] | None = None,
        **kwargs: Any,
    ) -> None:
        """Create an HTTPBot client."""
        self.http: HTTP
        self._token: str
        self._id: Final[int] = client_id
        self._on_startup: Callable[[], Coroutine[Any, Any, None]] | None = on_startup
        self._on_shutdown: Callable[[], Coroutine[Any, Any, None]] | None = on_shutdown
        self._public_key: Final[str] = client_public_key
        self._register_commands_on_startup = register_commands_on_startup
        self._fastapi = FastAPI(
            **DEFAULT_FASTAPI_KWARGS,
            **kwargs,
            on_startup=[self._setup],
            on_shutdown=[self._shutdown],
        )
        self._commands: dict[ApplicationCommandType, dict[str, Command]] = {
            ApplicationCommandType.CHAT_INPUT: {},
            ApplicationCommandType.USER: {},
            ApplicationCommandType.MESSAGE: {},
            ApplicationCommandType.PRIMARY_ENTRY_POINT: {},
        }
        self._uri_path: str = uri_path
        self._fastapi.add_api_route(
            path=self._uri_path,
            endpoint=self._interaction_http_callback,
            name="HTTP Interaction Bot entry point",
            methods=["POST"],
        )

    if TYPE_CHECKING:

        @overload
        def command(
            self,
            name: str,
            *,
            description: str | None = ...,
            allowed_contexts: list[InteractionContextType] | None = ...,
            integration_types: list[ApplicationIntegrationType] | None = ...,
            autocompletes: None = ...,
            command_type: Literal[
                ApplicationCommandType.USER,
                ApplicationCommandType.PRIMARY_ENTRY_POINT,
                ApplicationCommandType.MESSAGE,
            ] = ...,
            auto_defer: bool = ...,
            name_localisations: LocaleDict | None = ...,
            description_localisations: LocaleDict | None = ...,
            option_localisations: dict[str, Locale] | None = ...,
        ) -> Callable[..., Any]: ...

        @overload
        def command(
            self,
            name: str,
            *,
            description: str | None = ...,
            allowed_contexts: list[InteractionContextType] | None = ...,
            integration_types: list[ApplicationIntegrationType] | None = ...,
            autocompletes: dict[str, AutocompleteFunc] | None = ...,
            command_type: Literal[ApplicationCommandType.CHAT_INPUT] = ...,
            auto_defer: bool = ...,
            name_localisations: LocaleDict | None = ...,
            description_localisations: LocaleDict | None = ...,
            option_localisations: dict[str, Locale] | None = ...,
        ) -> Callable[..., Any]: ...

    def command(
        self,
        name: str,
        *,
        description: str | None = None,
        allowed_contexts: list[InteractionContextType] | None = None,
        integration_types: list[ApplicationIntegrationType] | None = None,
        autocompletes: dict[str, AutocompleteFunc] | None = None,
        command_type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT,
        auto_defer: bool = False,
        name_localisations: LocaleDict | None = None,
        description_localisations: LocaleDict | None = None,
        option_localisations: dict[str, Locale] | None = None,
    ):
        """Register a command with the bot."""

        if command_type not in self._commands:
            raise ValueError(f"Invalid command type {command_type}")

        def _decorator(func: Any):
            if not command_type == ApplicationCommandType.CHAT_INPUT and autocompletes is not None:
                raise ValueError("Autocompletes are only supported for `ApplicationCommandType.CHAT_INPUT` commands")

            self._commands[command_type][name] = Command(
                func=func,
                name=name,
                allowed_contexts=set(allowed_contexts) if allowed_contexts else None,
                integration_types=set(integration_types) if integration_types else None,
                description=description,
                command_type=command_type,  # pyright: ignore[reportCallIssue, reportArgumentType]
                autocompletes=autocompletes,
                auto_defer=auto_defer,
                name_localisations=name_localisations,
                description_localisations=description_localisations,
                option_localisations=option_localisations,
            )

        return _decorator

    def register_command(self, command: Command) -> None:
        """ Register a non-decorator command with the bot, or a command group. """
        self._commands[command.command_type][command._name] = command

    async def _verify_signature(self, request: Request) -> bool:
        signature: str | None = request.headers.get("X-Signature-Ed25519")
        timestamp: str | None = request.headers.get("X-Signature-Timestamp")
        if signature is None or timestamp is None:
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
        if request_json["type"] == InteractionType.PING:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=JSONResponseType(
                    type=InteractionResponseType.PONG,
                ),
            )
        elif request_json["type"] == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
            return await self.__process_autocompletes(request, request_json)
        return await self.__process_commands(request, request_json)

    async def ___create_interaction(self, request: Request, command: Command, data: dict[str, Any]) -> Interaction:
        return Interaction(request, data, self)

    async def ___get_command_data(self, request: Request, data: dict[str, Any]) -> CommandData | None:
        command_name: str | None = data.get("data", {}).get("name", None)
        command_type: ApplicationCommandType | None = data.get("data", {}).get("type", None)
        if command_type is None or command_name is None:
            return None
        if command_type not in self._commands:
            raise UnknownCommand(f"Unknown command type {command_type}")
        command = self._commands[command_type].get(command_name, None)
        if not command:
            return None

        interaction = await self.___create_interaction(request, command, data)
        return CommandData(command=command, options=data["data"].get("options", []), interaction=interaction)

    async def __process_commands(self, request: Request, data: dict[str, Any]) -> Any:
        command_data = await self.___get_command_data(request, data)
        if not command_data:
            error_message = f"Unknown command used: {data.get('data', {}).get('name', 'N/A')}"  # Add context to error
            raise UnknownCommand(error_message)  # Raise with more details for better logging or handling upstream
        command = command_data.command
        interaction = command_data.interaction
        options = command_data.options_formatted
        for option_name in options.keys():
            kwarg_type = command._func.__annotations__[option_name]
            option_value = options[option_name]
            if kwarg_type.__class__ == enum.EnumType:
                # sorry
                options[option_name] = getattr(kwarg_type, option_value)
        if command._auto_defer:
            await interaction.defer()

        command_options = command.options or {}
        for option_name, option_value in options.items():
            if command_options[option_name]._type == ApplicationCommandOptionType.ATTACHMENT:
                options[option_name] = Attachment.from_option(data["data"]["resolved"]["attachments"][option_value])
            elif command_options[option_name]._type == ApplicationCommandOptionType.CHANNEL:
                options[option_name] = interaction.resolved.channels[int(option_value)]
            elif command_options[option_name]._type == ApplicationCommandOptionType.ROLE:
                options[option_name] = interaction.resolved.roles[int(option_value)]
            elif command_options[option_name]._native_type == Member:
                options[option_name] = interaction.resolved.members[int(option_value)]
            elif command_options[option_name]._native_type == User:
                options[option_name] = interaction.resolved.users[int(option_value)]

        response = await command.invoke(interaction, **options)
        return await self.__process_response(response, interaction)

    async def __process_response(
        self,
        response: CommandResponse,
        interaction: Interaction,
    ) -> Any:
        if len(response.files) == 0:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=response.to_dict(),
            )

        if not interaction.deffered:
            await interaction.defer(
                with_message=True,
                ephemeral=response.ephemeral,
            )

        json_payload = response.to_dict()["data"]
        del json_payload["flags"]
        route = Route(
            url=f"/webhooks/{self._id}/{interaction._token}/messages/@original",
            json=json_payload,
            files=response.files,
        )
        await self.http.patch(route)

        return None

    async def __process_autocompletes(self, request: Request, data: dict[str, Any]) -> JSONResponse:
        command_data = await self.___get_command_data(request, data)
        if command_data:
            interaction = command_data.interaction
            options = command_data.options
            for option_name, option_data in options.items():
                if option_data.get("focused", False) == True:
                    autocomplete_func = command_data.command._autocompletes[option_name]
                    autocomplete_responses = await autocomplete_func(interaction, option_data["value"])
                    response = AutocompleteResponse(choices=autocomplete_responses)
                    return JSONResponse(content=response.to_dict())
        raise UnknownCommand(f"Unknown autocomplete used")

    async def _interaction_http_callback(self, request: Request) -> JSONResponse:
        verified_signature = await self._verify_signature(request)
        if not verified_signature:
            return ERROR_BAD_SIGNATURE_REQUEST

        return await self._handle_verified_interaction(request)

    async def register_commands(self) -> None:
        api_commands: list[dict[str, Any]] = [
            command.to_dict() for commands in self._commands.values() for command in commands.values()
        ]
        await self.http.put(
            Route(
                f"/applications/{self._id}/commands",
                json=api_commands,
            )
        )

    async def _setup(self) -> None:
        self.http = HTTP(token=self._token)
        if self._register_commands_on_startup:
            await self.register_commands()
        if self._on_startup is not None:
            await self._on_startup()

    async def _shutdown(self) -> None:
        if self._on_shutdown is not None:
            await self._on_shutdown()

    def start(self, token: str, **kwargs: Any) -> None:
        self._token = token
        uvicorn.run(app=self._fastapi, **kwargs)
