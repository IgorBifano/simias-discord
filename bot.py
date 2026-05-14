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
CANAL_CHAT = os.getenv("CANAL_CHAT", "")  # nome do canal compartilhado

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
# CONVERSATION HISTORY
#
# canal compartilhado  → chave = "channel:{channel_id}"  (todos veem)
# outros canais        → chave = "user:{user_id}"        (privado)
#
# Limite de 20 turnos por chave para não explodir o contexto
# =========================

conversation_history = {}
MAX_HISTORY = 20


def get_history_key(message):
    """Retorna a chave de histórico correta para a mensagem."""
    if CANAL_CHAT and message.channel.name == CANAL_CHAT:
        return f"channel:{message.channel.id}"
    return f"user:{message.author.id}"


def get_history(key):
    if key not in conversation_history:
        conversation_history[key] = []
    return conversation_history[key]


def trim_history(key):
    if len(conversation_history[key]) > MAX_HISTORY * 2:
        conversation_history[key] = conversation_history[key][-(MAX_HISTORY * 2):]

# =========================
# READY EVENT
# =========================

@client.event
async def on_ready():

    print("=" * 50)
    print(f"Simias conectado como {client.user}")
    if CANAL_CHAT:
        print(f"Canal compartilhado: #{CANAL_CHAT}")
    print("Primal Network online.")
    print("=" * 50)

# =========================
# MESSAGE EVENT
# =========================

@client.event
async def on_message(message):

    # Ignora mensagens do próprio bot
    if message.author == client.user:
        return

    # Debug logs
    print(f"[MSG] #{message.channel.name} | {message.author}: {message.content}")

    # Só responde quando mencionado
    if str(client.user.id) not in message.content:
        return

    try:

        # Remove mention da mensagem
        user_message = message.content.replace(
            f"<@{client.user.id}>",
            ""
        ).replace(
            f"<@!{client.user.id}>",
            ""
        ).strip()

        # Caso vazio
        if not user_message:
            user_message = "Diga algo."

        # Histórico correto (canal compartilhado ou privado)
        key = get_history_key(message)
        history = get_history(key)

        # Identifica quem falou no histórico compartilhado
        if key.startswith("channel:"):
            content = f"[{message.author.display_name}]: {user_message}"
        else:
            content = user_message

        history.append({
            "role": "user",
            "content": content
        })

        trim_history(key)

        # Thinking message
        thinking_message = await message.channel.send(
            random.choice(thinking_messages)
        )

        # Typing animation
        async with message.channel.typing():

            response = anthropic.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=history
            )

        # Parse da resposta
        reply = ""

        if hasattr(response, "content"):
            for block in response.content:
                if hasattr(block, "text"):
                    reply += block.text

        # Segurança
        if not reply.strip():
            reply = "O núcleo cognitivo retornou silêncio absoluto."

        # Salva resposta no histórico
        history.append({
            "role": "assistant",
            "content": reply
        })

        # Envia resposta — divide se passar do limite do Discord
        if len(reply) <= 1900:
            await thinking_message.edit(content=reply)
        else:
            await thinking_message.edit(content=reply[:1900])
            remaining = reply[1900:]
            while remaining:
                await message.channel.send(remaining[:1900])
                remaining = remaining[1900:]

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
