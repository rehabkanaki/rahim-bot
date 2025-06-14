import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# المتغيرات البيئية
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# إعدادات Flask
app = Flask(__name__)

# إعداد البوت وOpenAI
bot = Bot(token=TOKEN)
openai.api_key = OPENAI_API_KEY

# Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# تعريف الأوامر
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل لي أي رسالة وسأرد عليك باستخدام ChatGPT.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "❌ حدث خطأ أثناء الاتصال بـ OpenAI."
    await update.message.reply_text(reply)

# تعيين الهاندلرز
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# نقطة استقبال الويب هوك
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        
        return "ok"


# إعداد الويب هوك
async def setup_webhook():
    await bot.delete_webhook()
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Webhook set successfully")

if __name__ == "__main__":
    asyncio.run(setup_webhook())
    app.run(host="0.0.0.0", port=10000)
