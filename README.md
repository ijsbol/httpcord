# HTTPCord

A light weight feature-packed HTTP interactions API wrapper for Discord written in Python.

## Installation

`pip install --update httpcord`

## Important items
- [Get support for the project](.github/SUPPORT.md)
- [Community code of conduct](.github/CODE_OF_CONDUCT.md)
- [Contributor guidelines](.github/CONTRIBUTING.md)
- [Report a security vulnerability](.github/SECURITY.md)
- [See the projects governance](.github/GOVERNANCE.md)

## Examples

From `examples/*.py`

```py
import asyncio
from enum import StrEnum
from io import BytesIO
import random
from typing import Annotated

from httpcord import HTTPBot, CommandResponse, Interaction
from httpcord.command import Command
from httpcord.command.base import InteractionContextType
from httpcord.command.types import Choice
from httpcord.embed import Embed
from httpcord.enums import ApplicationCommandType, ApplicationIntegrationType, InteractionResponseType
from httpcord.member import Member
from httpcord.types import Integer, Float, String
from httpcord.attachment import Attachment
from httpcord.channel import BaseChannel
from httpcord.role import Role
from httpcord.file import File
from httpcord.locale import Locale
from httpcord.user import User


CLIENT_ID = 00000000000000000000
CLIENT_PUBLIC_KEY = "..."
CLIENT_TOKEN = "..."


bot = HTTPBot(
    client_id=CLIENT_ID,
    client_public_key=CLIENT_PUBLIC_KEY,
    register_commands_on_startup=True,
)


@bot.command("hello-world")
async def hello_world(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"hello, {interaction.user.mention}!",
    )

@bot.command("ephemeral")
async def ephemeral(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content="Hello!",
        ephemeral=True,
    )

@bot.command("guess-number")
async def guess_number(interaction: Interaction, *, guess: int, max_value: int = 10) -> CommandResponse:
    winning_number = random.randint(0, max_value)
    if guess == winning_number:
        return CommandResponse(
            type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            content="Yay! You guessed the number correctly :)",
        )
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content="Aww, you got the number wrong. Better luck next time :)",
    )

@bot.command("embed")
async def embed(interaction: Interaction) -> CommandResponse:
    embed = Embed(title="Embed title")
    embed.add_field(name="Embed field title 1", value="Embed field value 1", inline=False)
    embed.add_field(name="Embed field title 2", value="Embed field value 2", inline=False)
    embed.add_field(name="Embed field title 3", value="Embed field value 3", inline=True)
    embed.add_field(name="Embed field title 4", value="Embed field value 4", inline=True)
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        embeds=[embed],
    )

ANIMALS: list[str] = [
    "dog",
    "cat",
    "giraffe",
    "wolf",
    "parrot",
    "axolotl",
]


async def string_autocomplete(interaction: Interaction, current: str) -> list[Choice]:
    return [
        Choice(name=animal, value=animal)
        for animal in ANIMALS if current.lower() in animal
    ]


@bot.command(
    name="autocomplete",
    description="command with autocomplete",
    autocompletes={
        "string": string_autocomplete,
    },
)
async def autocomplete_command(interaction: Interaction, *, string: str) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        embeds=[Embed(title=string)],
    )

@bot.command("defer-me")
async def defer_me(interaction: Interaction) -> CommandResponse:
    await interaction.defer()
    await asyncio.sleep(3)
    await interaction.followup(CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Deferred message.",
    ))
    await interaction.followup(CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Second follow up message.",
    ))

    # You can return another followup message, or just a PONG if you want to do nothing else.
    return CommandResponse(InteractionResponseType.PONG)

@bot.command("hello-world-deferred", auto_defer=True)
async def hello_world_long(interaction: Interaction) -> CommandResponse:
    await asyncio.sleep(3)
    await interaction.followup(CommandResponse(
        type=InteractionResponseType.DEFERRED_UPDATE_MESSAGE,
        content=f"Hello, {interaction.user.mention}!",
    ))
    return CommandResponse(InteractionResponseType.PONG)

class Fruits(StrEnum):
    apples = "apples"
    cherries = "cherries"
    kiwis = "kiwis"
    oranges = "oranges"

@bot.command("pick")
async def pick(interaction: Interaction, *, fruit: Fruits) -> CommandResponse:
    return CommandResponse(
        InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"You picked: {fruit.value}!",
    )

async def group_sub_command(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Hello, world!",
    )

async def group_sub_sub_command(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Hello... mars?",
    )

command_group = Command(
    name="group-name",
    description="This is the group description",
    sub_commands=[
        Command(
            name="hello",
            description="Say hello!",
            func=group_sub_command,
        ),
        Command(
            name="sub-group",
            sub_commands=[
                Command(
                    name="wow",
                    description="This is awesome!",
                    func=group_sub_sub_command,
                ),
            ],
        ),
    ],
)

bot.register_command(command_group)

@bot.command("Ping the message author", command_type=ApplicationCommandType.MESSAGE)
async def message_command(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Hey, {interaction.user.mention}!",
    )

@bot.command("Say hello!", command_type=ApplicationCommandType.USER)
async def user_command(interaction: Interaction) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Hey, {interaction.user.mention}!",
    )

@bot.command("int-and-float-bounding")
async def int_and_float_bounding(
    interaction: Interaction,
    *,
    integer: Annotated[int, Integer(min_value=3, max_value=10)],
    number: Annotated[float, Float(min_value=0.5, max_value=2.5)],
) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Wow! {integer} and {number}",
    )

@bot.command("string-length-test")
async def string_length_test(
    interaction: Interaction,
    *,
    echo: Annotated[str, String(min_length=3, max_length=10)],
) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Wow! {echo}",
    )

@bot.command("user-upload-attachment")
async def user_upload_attachment(interaction: Interaction, *, attachment: Attachment) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"You uploaded a file with name: {attachment.filename}!",
    )

@bot.command(
    name="hello-world",
    name_localisations={
        "en-US": "hello-world",
        "fr": "bonjour-le-monde",
        "es-ES": "hola-mundo",
    },
    option_localisations={
        "parameter": Locale(description="This is a described parameter.")
    },
)
async def hello_world_translated(interaction: Interaction, *, parameter: str) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Hello, world!",
    )


@bot.command("get-channel")
async def get_channel(interaction: Interaction, *, channel: BaseChannel) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Channel {channel.id} selected.",
    )


@bot.command("get-user",
    allowed_contexts=[
        InteractionContextType.PRIVATE_CHANNEL,
        InteractionContextType.GUILD,
        InteractionContextType.BOT_DM,
    ],
    integration_types=[
        ApplicationIntegrationType.GUILD_INSTALL,
        ApplicationIntegrationType.USER_INSTALL,
    ],
)
async def get_user(interaction: Interaction, *, user: User) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"User {user} selected.",
    )


@bot.command("get-member",
    allowed_contexts=[
        InteractionContextType.PRIVATE_CHANNEL,
        InteractionContextType.GUILD,
        InteractionContextType.BOT_DM,
    ],
    integration_types=[
        ApplicationIntegrationType.GUILD_INSTALL,
        ApplicationIntegrationType.USER_INSTALL,
    ],
)
async def get_member(interaction: Interaction, *, member: Member) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"PartialMemberWithUser {member} selected.",
    )


@bot.command("get-role")
async def get_role(interaction: Interaction, *, role: Role) -> CommandResponse:
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"Role {role.id} selected.",
    )


@bot.command("attachment-response")
async def attachment_response(interaction: Interaction, *, attachment: Attachment) -> CommandResponse:
    attachment_request = await interaction.bot.http._session.get(attachment.url)
    attachment_data = await attachment_request.read()
    attachment_bytes = BytesIO(attachment_data)
    attachment_bytes.seek(0)
    return CommandResponse(
        type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        content=f"You uploaded an attachment with name: {attachment.filename}, i've attached it to this message!",
        files=[
            File(
                fp=attachment_bytes,
                filename=attachment.filename,
            )
        ]
    )


bot.start(token=CLIENT_TOKEN, port=8080)
```
