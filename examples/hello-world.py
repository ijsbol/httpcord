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


bot.start(CLIENT_TOKEN)