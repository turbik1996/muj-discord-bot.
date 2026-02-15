import discord
import os
from poe_api_wrapper import PoeApi

# Načtení tajných údajů z nastavení hostingu
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_POE = os.getenv("POE_TOKEN")
BOT_NA_POE = os.getenv("POE_BOT_NAME")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Přihlášení k Poe hned při startu (zrychlí bota)
poe_client = PoeApi(TOKEN_POE)

@client.event
async def on_ready():
    print(f'Bot {client.user} je online a připraven!')

@client.event
async def on_message(message):
    # Ignoruj zprávy od sebe sama
    if message.author == client.user:
        return

    # Bot odpoví, jen když ho někdo označí @Jméno
    if client.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Očištění zprávy od zmínky bota
                user_query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                
                odpoved = ""
                # Získání odpovědi z Poe
                for chunk in poe_client.send_message(BOT_NA_POE, user_query):
                    odpoved += chunk["text_new"]

                if odpoved:
                    await message.reply(odpoved)
                else:
                    await message.reply("Omlouvám se, ale nedostal jsem žádnou odpověď.")
            except Exception as e:
                await message.reply(f"Došlo k chybě: {e}")
                print(f"Chyba: {e}")

client.run(TOKEN_DISCORD)
