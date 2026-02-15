import discord
import os
from poe_api_wrapper import Client

# Načtení tajných údajů z nastavení hostingu
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_POE = os.getenv("POE_TOKEN")
# Název bota na Poe (např. "ChatGPT", "Claude-3-Haiku" nebo tvůj vlastní)
BOT_NA_POE = os.getenv("POE_BOT_NAME", "ChatGPT")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} je online a připraven na Koyebu!')

@client.event
async def on_message(message):
    # Ignoruj zprávy od sebe sama
    if message.author == client.user:
        return

    # Bot odpoví, jen když ho někdo označí @JménoBota
    if client.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Připojení k Poe
                poe_client = Client(TOKEN_POE)
                odpoved = ""
                
                # Očištění zprávy od zmínky bota
                user_query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                
                # Získání odpovědi
                for chunk in poe_client.send_message(BOT_NA_POE, user_query):
                    odpoved += chunk["text_new"]
                
                if odpoved:
                    await message.reply(odpoved)
                else:
                    await message.reply("Poe neodpovídá, zkus to znovu.")
                    
            except Exception as e:
                print(f"Chyba: {e}")
                await message.reply("Mám technické potíže s připojením k mozku.")

client.run(TOKEN_DISCORD)
