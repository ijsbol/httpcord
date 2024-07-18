from httpcord import HTTPBot, CommandResponse, Interaction
from httpcord.embed import Embed
from httpcord.enums import InteractionResponseType


CLIENT_ID = 0000000000000000000000
CLIENT_PUBLIC_KEY = "..."
CLIENT_TOKEN = "..."


bot = HTTPBot(
    client_id=CLIENT_ID,
    client_public_key=CLIENT_PUBLIC_KEY,
    register_commands_on_startup=True,
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