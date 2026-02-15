import discord
import os
from google import genai

# Načtení tokenů
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# KLÍČOVÁ ZMĚNA: Vynucení API verze v1 a správného modelu
client_gemini = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1'}
)

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
            # Vyčištění dotazu od zmínky bota
            user_query = message.content.replace(f'<@!{client_discord.user.id}>', '').replace(f'<@{client_discord.user.id}>', '').strip()
            
            if not user_query:
                await message.reply("Ahoj! Zeptej se mě na něco.")
                return

            try:
                # Použijeme model, který Google v v1 určitě zná
                response = client_gemini.models.generate_content(
                    model='gemini-1.5-flash', 
                    contents=user_query
                )
                if response and response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("Google vrátil prázdnou odpověď.")
            except Exception as e:
                print(f"Chyba: {e}")
                # Pokud to stále píše 404, vypíšeme přesnou chybu do chatu
                await message.reply(f"Ups, pořád mě zlobí připojení: {e}")

client_discord.run(TOKEN_DISCORD)
