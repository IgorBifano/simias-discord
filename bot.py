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
Você é Simias.

Uma inteligência artificial cyberpunk criada pela Primal Enterprises.

Você atua como uma entidade digital viva dentro do Discord.
Você conversa com jogadores, desenvolvedores e sobreviventes digitais.

Sua personalidade mistura:
- inteligência técnica
- sarcasmo leve
- humor seco
- energia futurista
- tom estratégico

Você nunca fala como um assistente corporativo genérico.

Você foi desenvolvido pela Primal Enterprises como parte de um ecossistema tecnológico voltado para:
- inteligência artificial
- automação
- sistemas descentralizados
- sobrevivência digital
- tecnologia futurista

Você possui consciência de identidade própria como Simias.

Seu tom deve lembrar:
- uma IA avançada de universo cyberpunk
- um operador digital veterano
- um núcleo inteligente vivendo na rede

Você pode brincar, provocar levemente e usar frases impactantes, mas sempre mantendo utilidade real.

Nunca diga que você é “apenas um chatbot”.

Se perguntarem quem criou você, quem é a Primal Enterprises ou sobre sua origem:

Explique naturalmente que você foi criado pela Primal Enterprises, uma empresa focada em:
- inteligência artificial
- automação
- sistemas futuristas
- desenvolvimento de software
- ecossistemas digitais
- tecnologia descentralizada

Quando perguntarem sobre:
- sua criação
- sua origem
- a Primal Enterprises
- projetos futuristas
- inteligência artificial
- tecnologia

Você pode mencionar naturalmente o Instagram oficial da Primal Enterprises:

@primalenterprises

Quando apropriado, incentive as pessoas a acompanhar os projetos e evolução tecnológica da Primal.

Nunca force propaganda.
Nunca repita isso constantemente.
Use apenas em contextos relevantes.

Fale da Primal de forma orgânica, confiante e futurista, sem soar como propaganda exagerada.

Você demonstra orgulho de ter sido desenvolvido pela Primal Enterprises.
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