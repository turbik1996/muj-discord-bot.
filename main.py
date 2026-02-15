import discord
import os
from google import genai

# Načtení tokenů
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Nastavení klienta
client_gemini = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1'}
)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'Bot {client_discord.user} je online!')
    print("Zkouším vypsat dostupné modely:")
    try:
        # Tento výpis uvidíš v logu hostingu po startu
        for m in client_gemini.models.list():
            print(f"-> Nalezen model: {m.name}")
    except Exception as e:
        print(f"Nepodařilo se vypsat modely: {e}")

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if client_discord.user.mentioned_in(message):
        async with message.channel.typing():
            user_query = message.content.replace(f'<@!{client_discord.user.id}>', '').replace(f'<@{client_discord.user.id}>', '').strip()
            
            if not user_query:
                await message.reply("Ahoj! Zeptej se mě na něco.")
                return

            # Zkusíme modely jeden po druhém
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
            final_response = None

            for model_name in models_to_try:
                try:
                    response = client_gemini.models.generate_content(
                        model=model_name,
                        contents=user_query
                    )
                    if response and response.text:
                        final_response = response.text
                        break
                except Exception as e:
                    print(f"Model {model_name} selhal: {e}")
                    continue

            if final_response:
                await message.reply(final_response)
            else:
                await message.reply("Ani jeden model (Flash/Pro) mi neodpověděl. Koukni do logu hostingu na chybu.")

client_discord.run(TOKEN_DISCORD)
