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

from enum import IntEnum
from typing import Final


__all__: Final[tuple[str, ...]] = (
    "ApplicationCommandType",
    "InteractionType",
    "InteractionResponseType",
    "InteractionContextType",
    "InteractionResponseFlags",
    "ApplicationCommandOptionType",
    "ApplicationIntegrationType",
)


class ApplicationCommandType(IntEnum):
    '''Enum for different types of application commands in Discord interactions.'''
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3
    PRIMARY_ENTRY_POINT = 4


class InteractionType(IntEnum):
    '''Enum for types of interactions received from Discord.'''
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class InteractionContextType(IntEnum):
    '''Enum for contexts in which interactions can occur.'''
    GUILD = 0
    BOT_DM = 1
    PRIVATE_CHANNEL = 2


class InteractionResponseType(IntEnum):
    '''Enum for types of responses to interactions.'''
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


class InteractionResponseFlags(IntEnum):
    '''Enum for flags used in interaction responses, such as making them ephemeral.'''
    EPHEMERAL = 1 << 6


class ApplicationCommandOptionType(IntEnum):
    '''Enum for types of options in application commands.'''
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4     # Any integer between -2^53 and 2^53
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7     # Includes all channel types + categories
    ROLE = 8
    MENTIONABLE = 9 # Includes users and roles
    NUMBER = 10	    # Any double between -2^53 and 2^53
    ATTACHMENT = 11 # attachment object


class ApplicationIntegrationType(IntEnum):
    '''Enum for types of application integrations.'''
    GUILD_INSTALL = 0
    USER_INSTALL = 1
