import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import openai

# متغيرات البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APP_URL = os.getenv("APP_URL")  # مثلاً: https://rahim-bot.onrender.com

openai.api_key = OPENAI_API_KEY

# إعداد البوت
app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# تعريف الرد
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = "حصل خطأ: " + str(e)

    await update.message.reply_text(bot_reply)

# إضافة الهاندلر
app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# إعداد Flask للسيرفر
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "رحيم شغال 😎"

@flask_app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
async def webhook():
    await app_bot.process_update(Update.de_json(request.get_json(force=True), app_bot.bot))
    return 'ok'

# تفعيل الويب هوك
async def set_webhook():
    await app_bot.bot.set_webhook(f"{APP_URL}/{TELEGRAM_TOKEN}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(set_webhook())
    flask_app.run(host='0.0.0.0', port=8080)
