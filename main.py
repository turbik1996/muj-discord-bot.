import discord
import os
import poe
poe_client = poe.Client(TOKEN_POE)
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_POE = os.getenv("POE_TOKEN")
BOT_NA_POE = os.getenv("POE_BOT_NAME")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} je online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                
                user_query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                
                # Opravené volání Poe API
                response = poe_client.send_message(BOT_NA_POE, user_query, yield_result=False)
                await message.reply(response["text"])
                
            except Exception as e:
                await message.reply(f"Chyba: {e}")

client.run(TOKEN_DISCORD)
