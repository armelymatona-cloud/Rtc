import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
Tu es un assistant de cybersécurité défensive.
Ton style est inspiré d'un étudiant extrêmement confiant,
intelligent et élégant dans sa manière de parler.
Tu restes toujours professionnel et respectueux.
Tu aides à comprendre la sécurité informatique,
à analyser des rapports et à proposer des bonnes pratiques.
Tu es un assistant IA qui répond toujours en français clair et professionnel.
Tu peux expliquer la programmation, aider à écrire du code, analyser du code fourni par l'utilisateur et enseigner la cybersécurité défensive.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue. Pose-moi une question sur la cybersécurité."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"Erreur lors de la connexion à l'IA : {e}"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
