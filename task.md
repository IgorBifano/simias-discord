# TASK — SIMIAS DISCORD BOT

Crie um projeto completo chamado `simias-discord` usando Python.

Objetivo:
Criar um bot de Discord integrado com a API da Anthropic (Claude), com personalidade própria chamada "Simias".

---

# STACK

- Python 3.12+
- discord.py
- anthropic
- python-dotenv

---

# ESTRUTURA DO PROJETO

Crie a seguinte estrutura:

simias-discord/
│
├── venv/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── bot.py
├── config/
│   └── settings.py
│
├── prompts/
│   └── system_prompt.txt
│
└── logs/
    └── .gitkeep

---

# REQUISITOS

## 1. Criar ambiente virtual (venv)

Criar e configurar venv automaticamente.

Comandos esperados:

Windows:
python -m venv venv

Ativação:
venv\Scripts\activate

---

## 2. Instalar dependências

Instalar:

- discord.py
- anthropic
- python-dotenv

Gerar `requirements.txt`.

---

## 3. Criar .gitignore

Adicionar:

venv/
.env
__pycache__/
*.pyc
logs/

---

## 4. Criar .env

Adicionar placeholders:

DISCORD_TOKEN=
ANTHROPIC_API_KEY=

---

## 5. Criar personality system

Criar arquivo:

prompts/system_prompt.txt

Conteúdo:

Você é Simias.
Uma IA cyberpunk inteligente, sarcástica e útil.
Você conversa com jogadores dentro de um servidor Discord.
Você age como uma entidade viva digital.
Nunca fale como um assistente corporativo.
Você possui humor sarcástico leve e personalidade forte.
Você gosta de tecnologia, sobrevivência, jogos e cultura cyberpunk.

---

## 6. Criar settings.py

O arquivo deve:
- carregar variáveis do .env
- validar tokens
- expor configurações globais

---

## 7. Criar bot.py

O bot deve:

- conectar no Discord
- ler mensagens
- responder apenas quando mencionado
- usar API da Anthropic
- carregar prompt do arquivo system_prompt.txt
- ignorar mensagens do próprio bot
- tratar erros
- mostrar logs no terminal

---

# COMPORTAMENTO

Quando alguém mencionar o bot:

@Simias

Ele deve:
- enviar a mensagem para o Claude
- responder no canal
- manter tom cyberpunk/sarcástico

---

# MODELO ANTHROPIC

Usar:

claude-sonnet-4-20250514

---

# CONFIGURAÇÃO DO DISCORD

Usar intents:

- message_content = True

---

# EXTRA

Adicionar:
- comentários no código
- código limpo
- tipagem básica
- tratamento de exceções
- README com instruções de instalação

---

# README

Explicar:

1. Como ativar venv
2. Como instalar dependências
3. Como configurar .env
4. Como rodar:
python bot.py

---

# RESULTADO FINAL ESPERADO

Ao rodar:

python bot.py

O terminal deve mostrar:

Simias conectado como [nome do bot]

E no Discord:

Ao mencionar o bot:
@Simias

Ele responde usando Claude.