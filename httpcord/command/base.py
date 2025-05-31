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

import enum
import types
from typing import (
    Any,
    Final,
    Literal,
    overload,
)

from rich import TYPE_CHECKING

from httpcord.command.types import Choice, CommandOption
from httpcord.enums import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    ApplicationIntegrationType,
    InteractionContextType,
    InteractionResponseType,
)
from httpcord.func_protocol import AutocompleteFunc, CommandFunc
from httpcord.interaction import CommandResponse, Interaction
from httpcord.locale import DEFAULT_LOCALE, Locale, LocaleDict
from httpcord.types import (
    TYPE_CONVERSION_TABLE,
    Float,
    Integer,
    String,
)


__all__: Final[tuple[str, ...]] = (
    "Command",
    "CommandData",
    "AutocompleteResponse",
)


class Command:
    __slots__: Final[tuple[str, ...]] = (
        "_func",
        "_name",
        "_command_type",
        "_description",
        "_autocompletes",
        "_auto_defer",
        "_sub_commands",
        "_is_sub_command_group",
        "_allowed_contexts",
        "_integration_types",
        "_locale",
        "_option_localisations",
    )

    if TYPE_CHECKING:
        @overload
        def __init__(
            self,
            *,
            name: str,
            command_type: Literal[
                ApplicationCommandType.MESSAGE,
                ApplicationCommandType.PRIMARY_ENTRY_POINT,
                ApplicationCommandType.USER,
            ] = ...,
            allowed_contexts: set[InteractionContextType] | None = ...,
            integration_types: set[ApplicationIntegrationType] | None = ...,
            description: None = ...,
            func: CommandFunc | None = ...,
            autocompletes: None = ...,
            auto_defer: bool = ...,
            sub_commands: None = ...,
            name_localisations: LocaleDict | None = ...,
            description_localisations: LocaleDict | None = ...,
            option_localisations: dict[str, Locale] | None = ...,
        ) -> None: ...

        @overload
        def __init__(
            self,
            *,
            name: str,
            command_type: Literal[ApplicationCommandType.CHAT_INPUT] = ...,
            allowed_contexts: set[InteractionContextType] | None = ...,
            integration_types: set[ApplicationIntegrationType] | None = ...,
            description: str | None = ...,
            func: CommandFunc | None = ...,
            autocompletes: dict[str, AutocompleteFunc] | None = ...,
            auto_defer: bool = ...,
            sub_commands: None = ...,
            name_localisations: LocaleDict | None = ...,
            description_localisations: LocaleDict | None = ...,
            option_localisations: dict[str, Locale] | None = ...,
        ) -> None: ...

        @overload
        def __init__(
            self,
            *,
            name: str,
            command_type: Literal[ApplicationCommandType.CHAT_INPUT] = ...,
            allowed_contexts: set[InteractionContextType] | None = ...,
            integration_types: set[ApplicationIntegrationType] | None = ...,
            description: str | None = ...,
            func: None = ...,
            autocompletes: None = ...,
            auto_defer: None = ...,
            sub_commands: list[Command] = ...,
            name_localisations: LocaleDict | None = ...,
            description_localisations: LocaleDict | None = ...,
            option_localisations: dict[str, Locale] | None = ...,
        ) -> None: ...

    def __init__(
        self,
        *,
        name: str,
        command_type: ApplicationCommandType | None = None,
        allowed_contexts: set[InteractionContextType] | None = None,
        integration_types: set[ApplicationIntegrationType] | None = None,
        description: str | None = None,
        func: CommandFunc | None = None,
        autocompletes: dict[str, AutocompleteFunc] | None = None,
        auto_defer: bool | None = False,
        sub_commands: list[Command] | None = None,
        name_localisations: LocaleDict | None = None,
        description_localisations: LocaleDict | None = None,
        option_localisations: dict[str, Locale] | None = None,
    ) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Command name must be a non-empty string.')
        if sub_commands is not None and not all(isinstance(sub, Command) for sub in sub_commands):
            raise ValueError('Sub-commands must be a list of Command objects.')
        if (func is None and sub_commands is None) or (func is None and len(sub_commands or []) == 0):
            raise ValueError(f"Group command must have at least one sub command provided (`{name}`).")

        self._func: CommandFunc | None = func
        self._name: str = name
        self._description: str | None = description
        self._integration_types: set[ApplicationIntegrationType] = integration_types or {
            ApplicationIntegrationType.GUILD_INSTALL,
        }
        self._allowed_contexts: set[InteractionContextType] = allowed_contexts or {
            InteractionContextType.BOT_DM,
            InteractionContextType.GUILD,
            InteractionContextType.PRIVATE_CHANNEL,
        }
        self._locale: Locale = Locale(
            name_localisations=name_localisations,
            description_localisations=description_localisations,
        )
        self._option_localisations: dict[str, Locale] = option_localisations or {}
        self._command_type: ApplicationCommandType = command_type or ApplicationCommandType.CHAT_INPUT
        self._autocompletes: dict[str, AutocompleteFunc] = autocompletes or {}
        self._auto_defer: bool = auto_defer or False
        self._sub_commands: dict[str, Command] = {
            sub_command.name: sub_command
            for sub_command in (sub_commands or [])
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def command_type(self) -> ApplicationCommandType:
        return self._command_type

    @property
    def description(self) -> str | None:
        return (
            (self._description or "--")
            if self.command_type == ApplicationCommandType.CHAT_INPUT
            else None
        )

    @property
    def autocompletes(self) -> dict[str, AutocompleteFunc]:
        return self._autocompletes

    @property
    def auto_defer(self) -> bool:
        return self._auto_defer

    @property
    def is_sub_command_group(self) -> bool:
        return len(self._sub_commands) > 0

    @property
    def allowed_contexts(self) -> set[InteractionContextType]:
        return self._allowed_contexts

    @property
    def integration_types(self) -> set[ApplicationIntegrationType]:
        return self._integration_types

    @property
    def options(self) -> dict[str, CommandOption] | None:
        if self._func is None and len(self._sub_commands) == 0:
            return None
        options: dict[str, CommandOption] = {}
        if self._func is not None:
            raw_options = list(self._func.__annotations__.items())[1:-1]
            default_options: dict[str, Any] = getattr(self._func, "__kwdefaults__") or {}
            for option_name, option_value in raw_options:
                required = not option_name in default_options
                choices: list[Choice] | None = None
                if type(option_value) == types.UnionType:
                    option_value = option_value.__args__[0]
                if option_value.__class__ == enum.EnumType:
                    choices = [
                        Choice(name=v.value, value=k)
                        for k, v in option_value.__members__.items()
                    ]
                    option_value = option_value.__base__.__bases__[0]
                option_settings: dict[str, Any] = {}
                annotation_settings = getattr(option_value, "__dict__", {})
                if annotation_settings.get('_name') == "Annotated":
                    if annotation_settings.get('__metadata__', None) is not None:
                        annotated_type = annotation_settings['__metadata__'][0]
                        option_value = annotation_settings['__origin__']
                        if type(annotated_type) in (Integer, Float):
                            option_settings = {
                                "min_value": annotated_type.min_value,
                                "max_value": annotated_type.max_value,
                            }
                        elif type(annotated_type) in (String,):
                            option_settings = {
                                "min_length": annotated_type.min_length,
                                "max_length": annotated_type.max_length,
                            }

                if option_value not in TYPE_CONVERSION_TABLE.keys():
                    option_value = str

                option_description = None
                option_localiser = self._option_localisations.get(option_name, None)
                if option_localiser is not None:
                    option_description = option_localiser.get_default("description_localisations")
                options[option_name] = CommandOption(  # pyright: ignore[reportCallIssue]
                    name=option_name,
                    description=option_description,
                    type=TYPE_CONVERSION_TABLE[option_value],  # type: ignore[reportArgumentType]
                    required=required,
                    autocomplete=option_name in self._autocompletes.keys(),  # type: ignore[reportArgumentType]
                    options=None,
                    choices=choices,
                    locale=self._option_localisations.get(option_name, None),
                    **option_settings,
                )
            return options
        for name, command in self._sub_commands.items():
            if command.is_sub_command_group:
                if not command.options:
                    raise ValueError(f"Subcommand group `{self.name} {command.name}` must have sub commands provided.")
                options[name] = CommandOption(
                    name=name,
                    description=command.description,
                    type=ApplicationCommandOptionType.SUB_COMMAND_GROUP,
                    required=None,
                    autocomplete=None,
                    options=command.options,
                    choices=None,
                )
                continue
            options[name] = CommandOption(
                name=name,
                description=command.description,
                type=ApplicationCommandOptionType.SUB_COMMAND,
                required=None,
                autocomplete=False,
                options=command.options,
                choices=None,
            )
        return options

    async def invoke(self, interaction: Interaction, **kwargs: Any) -> CommandResponse:
        if self._func is None:
            raise ValueError("This command cannot be directly invoked.")

        return await self._func(interaction, **kwargs)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.command_type.value,
            "description": self.description,
            "integration_types": [integration_type.value for integration_type in self.integration_types],
            "contexts": [context.value for context in self.allowed_contexts],
            "options": [option.to_dict() for option in self.options.values()] if self.options else None,
            "name_localizations": self._locale.name_localisations,
            "description_localizations": self._locale.description_localisations,
        }


class CommandData:
    __slots__: Final[tuple[str, ...]] = (
        "command",
        "options",
        "options_formatted",
        "interaction",
    )

    def _extract_to_base_command(
        self,
        command: Command,
        options: list[dict[str, Any]],
    ) -> tuple[Command, list[dict[str, Any]]]:
        if command.is_sub_command_group:
            for sub_command in command._sub_commands.values():
                if sub_command.name == options[0]['name']:
                    command = sub_command
                    options = options[0]['options']
        return command, options

    def __init__(
        self,
        command: Command,
        options: list[dict[str, Any]],
        interaction: Interaction,
    ) -> None:
        while command.is_sub_command_group:
            command, options = self._extract_to_base_command(command, options)

        self.command: Command = command
        self.options: dict[str, Any] = {o['name']: o for o in options}
        self.options_formatted: dict[str, Any] = {o['name']: o['value'] for o in options}
        self.interaction: Interaction = interaction


class AutocompleteResponse:
    __slotst__: Final[tuple[str, ...]] = (
        "choices",
    )

    def __init__(self, choices: list[Choice]) -> None:
        self.choices: list[Choice] = choices

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
            "data": {"choices": [dict(choice) for choice in self.choices][:25]},
        }
