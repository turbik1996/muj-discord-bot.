import discord
import os
from google import genai

# Načtení tokenů z Environment variables
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Nastavení klienta s explicitním vynucením verze 'v1'
client_gemini = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1'}
)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'Bot {client_discord.user} je online a verze API je v1!')

@client_discord.event
async def on_message(message):
    # Ignoruj zprávy od bota samotného
    if message.author == client_discord.user:
        return

    # Reaguj na zmínku
    if client_discord.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Očištění dotazu
                user_query = message.content.replace(f'<@!{client_discord.user.id}>', '').replace(f'<@{client_discord.user.id}>', '').strip()
                
                if not user_query:
                    await message.reply("Ahoj! Zeptej se mě na něco.")
                    return

                # Volání Gemini
                # Seznam modelů, které zkusíme postupně
                models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
                response = None
                
                for model_name in models_to_try:
                    try:
                        response = client_gemini.models.generate_content(
                            model=model_name,
                            contents=user_query
                        )
                        if response:
                            break # Pokud se to povedlo, vyskočíme z cyklu
                    except:
                        continue # Pokud tento model nefunguje, zkusíme další
                
                if response:
                    await message.reply(response.text)
                else:
                    await message.reply("Bohužel ani jeden z modelů (Flash, Pro) neodpovídá. Zkontroluj prosím limity v Google AI Studio.")
