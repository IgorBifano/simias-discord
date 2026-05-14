import os
import random
import traceback
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
# CHECK ENV
# =========================

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN não encontrado.")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY não encontrada.")

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
intents.guilds = True
intents.members = True

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

Mantenha respostas naturais, inteligentes e levemente provocativas.
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
# READY EVENT
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

    # Debug
    print(f"[MSG] {message.author}: {message.content}")

    # Detecta mention do bot
    if str(client.user.id) in message.content:

        try:

            # Remove mention
            user_message = message.content.replace(
                f"<@{client.user.id}>",
                ""
            ).replace(
                f"<@!{client.user.id}>",
                ""
            ).strip()

            # Fallback
            if not user_message:
                user_message = "Diga algo."

            # Mensagem thinking
            thinking_message = await message.channel.send(
                random.choice(thinking_messages)
            )

            # Typing animation
            async with message.channel.typing():

                response = anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                )

            # Parse resposta
            reply = ""

            if hasattr(response, "content"):

                for block in response.content:

                    if hasattr(block, "text"):
                        reply += block.text

            # Fallback vazio
            if not reply.strip():
                reply = (
                    "O núcleo cognitivo retornou silêncio absoluto."
                )

            # Limite Discord
            reply = reply[:1900]

            # Edita mensagem thinking
            await thinking_message.edit(
                content=reply
            )

        except Exception as error:

            print("\n========== ERRO SIMIAS ==========")
            traceback.print_exc()
            print("=================================\n")

            await message.channel.send(
                f"Erro ao acessar núcleo cognitivo do Simias.\n```{error}```"
            )

# =========================
# START BOT
# =========================

client.run(DISCORD_TOKEN)