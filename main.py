import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# استدعاء المتغيرات من البيئة
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# إعدادات Flask
app = Flask(__name__)

# إعداد البوت وOpenAI
bot = Bot(token=TOKEN)
openai.api_key = OPENAI_API_KEY

# تعريف أوامر البوت
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

# نقطة الاستقبال من تليقرام
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.bot_app.process_update(update)
    return "ok"

# تشغيل التطبيق
if __name__ == "__main__":
    # بناء تطبيق التيليجرام
    app.bot_app = ApplicationBuilder().token(TOKEN).build()

    # إضافة المعالجات
    app.bot_app.add_handler(CommandHandler("start", start))
    app.bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # حذف الوِب هوك القديم وتعيين الجديد
    bot.delete_webhook()
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Webhook set successfully")

    # تشغيل Flask
    app.run(host="0.0.0.0", port=10000)

