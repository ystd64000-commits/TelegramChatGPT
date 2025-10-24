import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================= CONFIG ==================
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

openai.api_key = OPENAI_API_KEY
# ==========================================

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "សួស្តី! 🤖\n"
        "ខ្ញុំជាបតដែលអាចឆ្លើយសារដូច ChatGPT និងបកប្រែភាសា។\n"
        "Commands available:\n"
        "/translate <text> <language_code> → បកប្រែ\n"
        "ផ្ញើសារមកខ្ញុំ ដើម្បី chat ជាមួយ bot។"
    )

# Handle chat messages
async def chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("កំពុងឆ្លើយ... ⏳")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=500,
            temperature=0.7
        )
        reply_text = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"មានបញ្ហា: {e}")

# Handle translation
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /translate <text> <language_code>\nExample: /translate Hello km")
        return
    text_to_translate = " ".join(args[:-1])
    target_lang = args[-1]

    await update.message.reply_text("កំពុងបកប្រែ... ⏳")
    try:
        prompt = f"Translate the following text to {target_lang}:\n{text_to_translate}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )
        translated_text = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(f"Translated: {translated_text}")
    except Exception as e:
        await update.message.reply_text(f"មានបញ្ហា: {e}")

# MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
