import asyncio

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

@bot.command("hello-world-deferred", auto_defer=True)
async def hello_world_long(interaction: Interaction) -> CommandResponse:
    await asyncio.sleep(3)
    await interaction.followup(CommandResponse(
        type=InteractionResponseType.DEFERRED_UPDATE_MESSAGE,
        content=f"Hello, {interaction.user.mention}!",
    ))
    return CommandResponse(InteractionResponseType.PONG)

bot.start(CLIENT_TOKEN)