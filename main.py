import discord
import os
import google.generativeai as genai

# Načtení tokenů
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Nastavení Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
                response = model.generate_content(user_query)
                await message.reply(response.text)

            except Exception as e:
                print(f"Chyba: {e}")
                await message.reply(f"Ups, něco se pokazilo: {e}")

client.run(TOKEN_DISCORD)
