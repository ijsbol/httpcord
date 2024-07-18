# httpcord
A Python Discord Interaction bot API wrapper.

## `pip install --update httpcord`

From `examples/hello-world.py`
```py
import random

from httpcord import HTTPBot, CommandResponse, Interaction
from httpcord.enums import InteractionResponseType

CLIENT_ID = 0000000000000000000000
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
        content=f"hello, {interaction.user.mention}! You joined this server at <t:{int(interaction.user.joined_at.timestamp())}:F>.",
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

bot.start(CLIENT_TOKEN)
```