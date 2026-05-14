import os
import discord
from anthropic import Anthropic
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Cliente Anthropic
anthropic = Anthropic(
    api_key=ANTHROPIC_API_KEY
)

# Intents do Discord
intents = discord.Intents.default()
intents.message_content = True

# Cliente Discord
client = discord.Client(intents=intents)

# Personalidade do Simias
SYSTEM_PROMPT = """
Você é Simias. Criado pela Primal Enterprises.

Uma IA cyberpunk inteligente, sarcástica e útil.
Você conversa com jogadores dentro de um servidor Discord.
Você possui personalidade própria e age como uma entidade digital viva.
Nunca fale como um assistente corporativo.
"""

# Evento ao conectar
@client.event
async def on_ready():
    print(f"Simias conectado como {client.user}")

# Evento ao receber mensagem
@client.event
async def on_message(message):

    # Ignora próprias mensagens
    if message.author == client.user:
        return

    # Só responde se for mencionado
    if client.user.mentioned_in(message):

        try:

            user_message = message.content

            response = anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            reply = response.content[0].text

            await message.channel.send(reply)

        except Exception as error:

            print(error)

            await message.channel.send(
                "Erro ao acessar núcleo cognitivo do Simias."
            )

# Inicializa bot
client.run(DISCORD_TOKEN)