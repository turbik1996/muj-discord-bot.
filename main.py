import discord
import os
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# Načtení tokenů
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Nastavení Gemini s vynucením stabilní verze v1
genai.configure(api_key=GEMINI_API_KEY)

# Tady je ta změna - vytvoříme model, ale při generování mu vnutíme stabilní verzi
model = genai.GenerativeModel('gemini-1.5-flash')

# ... zbytek kódu (intents, client) zůstává stejný ...
intents = discord.Intents.default()
# ... atd.

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} je online s Gemini!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Očištění dotazu
                user_query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                
                if not user_query:
                    await message.reply("Ahoj! Zeptej se mě na něco.")
                    return

                # Generování odpovědi
               # Vynucení verze v1 při každém dotazu
response = model.generate_content(user_query, request_options=RequestOptions(api_version='v1'))
                await message.reply(response.text)

            except Exception as e:
                print(f"Chyba: {e}")
                await message.reply(f"Ups, něco se pokazilo: {e}")

client.run(TOKEN_DISCORD)
