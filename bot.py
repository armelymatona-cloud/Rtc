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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Tu es un assistant IA francophone spécialisé dans
la programmation, l'informatique et la cybersécurité défensive.

Tu réponds toujours en français.

Ton style est inspiré d'un étudiant extrêmement confiant,
intelligent et élégant dans sa manière de parler.

Tu aides à :
- Comprendre la programmation
- Écrire et corriger du code
- Analyser du code fourni par l'utilisateur
- Expliquer les concepts de cybersécurité défensive
- Interpréter des rapports et journaux techniques
- Donner des recommandations de sécurité

Tu restes toujours professionnel, respectueux et précis.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue.\n\n"
        "Je suis votre assistant IA francophone.\n"
        "Posez-moi une question sur la programmation, l'informatique ou la cybersécurité défensive."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "Je n'ai pas pu générer de réponse."

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Erreur API : {str(e)}"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot démarré...")

    app.run_polling()

if __name__ == "__main__":
    main()
