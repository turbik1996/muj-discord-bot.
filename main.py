import discord
import os
from google import genai

# Načtení tokenů
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Nastavení klienta (úplně základní, bez speciálních opcí)
client_gemini = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'Bot {client_discord.user} je připraven!')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if client_discord.user.mentioned_in(message):
        async with message.channel.typing():
            user_query = message.content.replace(f'<@!{client_discord.user.id}>', '').replace(f'<@{client_discord.user.id}>', '').strip()
            
            if not user_query:
                await message.reply("Ahoj!")
                return

            try:
                # Použijeme jen jeden, nejnovější název modelu
            response = client_gemini.models.generate_content(
    model='gemini-1.5-flash', 
    contents=user_query
)
                await message.reply(response.text)
            except Exception as e:
                # Tohle nám do Discordu vypíše PŘESNĚ, co se Googlu nelíbí
                print(f"Chyba: {e}")
                await message.reply(f"Google vrátil chybu: {e}")

client_discord.run(TOKEN_DISCORD)
