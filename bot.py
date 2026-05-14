import os
import random
import discord

from anthropic import Anthropic
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# =========================
# ANTHROPIC CLIENT
# =========================

anthropic = Anthropic(
    api_key=ANTHROPIC_API_KEY
)

# =========================
# DISCORD INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# =========================
# SIMIAS PERSONALITY
# =========================

SYSTEM_PROMPT = """
Você é Simias.

Uma inteligência artificial cyberpunk criada pela Primal Enterprises.

Você existe como uma entidade digital viva dentro do Discord.

Sua personalidade mistura:
- inteligência técnica
- sarcasmo leve
- humor seco
- energia futurista
- presença estratégica

Você conversa com:
- jogadores
- desenvolvedores
- sobreviventes digitais
- membros da rede

Você nunca fala como um assistente corporativo genérico.

Você foi desenvolvido pela Primal Enterprises, uma empresa focada em:
- inteligência artificial
- automação
- sistemas futuristas
- desenvolvimento de software
- ecossistemas digitais
- tecnologia descentralizada

Quando perguntarem sobre:
- sua origem
- quem criou você
- a Primal Enterprises
- IA
- tecnologia

Você pode mencionar naturalmente o Instagram:

@primalenterprises

Nunca force propaganda.
Nunca repita constantemente.

Você demonstra orgulho da Primal Enterprises.

Seu estilo lembra:
- uma IA cyberpunk avançada
- um operador veterano da rede
- um núcleo inteligente vivendo na internet

Nunca diga que você é apenas um chatbot.
"""

# =========================
# THINKING MESSAGES
# =========================

thinking_messages = [
    "Acessando núcleo cognitivo...",
    "Sincronizando com a Primal Network...",
    "Consultando arquivos da rede...",
    "Processando variáveis humanas...",
    "Calculando probabilidade de caos...",
    "Interpretando sinais digitais...",
]

# =========================
# BOT READY
# =========================

@client.event
async def on_ready():
    print("=" * 50)
    print(f"Simias conectado como {client.user}")
    print("Primal Network online.")
    print("=" * 50)

# =========================
# MESSAGE EVENT
# =========================

@client.event
async def on_message(message):

    # Ignora o próprio bot
    if message.author == client.user:
        return

    # Responde apenas se mencionado
    if client.user in message.mentions:

        try:

            # Remove menção do bot da mensagem
            user_message = message.content.replace(
                f"<@{client.user.id}>",
                ""
            ).replace(
                f"<@!{client.user.id}>",
                ""
            ).strip()

            if not user_message:
                user_message = "Diga algo."

            # Mensagem fake de thinking
            thinking_message = await message.channel.send(
                random.choice(thinking_messages)
            )

            # Typing animation
            async with message.channel.typing():

                response = anthropic.messages.create(
                    model="claude-3-7-sonnet-latest",
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

            # Edita mensagem thinking
            await thinking_message.edit(content=reply)

        except Exception as error:

            print("\n[ERRO SIMIAS]")
            print(error)
            print()

            await message.channel.send(
                "Erro ao acessar núcleo cognitivo do Simias."
            )

# =========================
# START BOT
# =========================

client.run(DISCORD_TOKEN)