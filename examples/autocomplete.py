from typing import Final
from httpcord import HTTPBot, CommandResponse, Interaction
from httpcord.embed import Embed
from httpcord.enums import InteractionResponseType
from httpcord.types import Choice


CLIENT_ID = 0000000000000000000000
CLIENT_PUBLIC_KEY = "..."
CLIENT_TOKEN = "..."


bot = HTTPBot(
    client_id=CLIENT_ID,
    client_public_key=CLIENT_PUBLIC_KEY,
    register_commands_on_startup=True,
)

ANIMALS: Final[list[str]] = [
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

bot.start(CLIENT_TOKEN)