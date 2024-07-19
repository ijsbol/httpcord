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

@bot.command("defer-me")
async def defer_me(interaction: Interaction) -> CommandResponse:
    await interaction.defer()
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


bot.start(CLIENT_TOKEN)