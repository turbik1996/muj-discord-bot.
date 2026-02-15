import discord
import os
import poe

# Načtení tokenů z Koyebu
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_POE = os.getenv("POE_TOKEN")  # TADY BUDE JEN TEN TVŮJ P-B TOKEN
BOT_NA_POE = os.getenv("POE_BOT_NAME")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} běží!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Inicializace klienta přímo ve zprávě (jednodušší pro start)
                poe_client = poe.Client(TOKEN_POE)
                
                user_query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                
                odpoved = ""
                for chunk in poe_client.send_message(BOT_NA_POE, user_query):
                    odpoved = chunk["text"] # Tato knihovna vrací celý text v chunk["text"]

                await message.reply(odpoved)
            except Exception as e:
                await message.reply(f"Chyba: {e}")
                print(f"Chyba: {e}")

client.run(TOKEN_DISCORD)
