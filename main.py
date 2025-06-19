import os
import openai
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# تحميل المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APP_URL = os.getenv("APP_URL")

# تهيئة البوت
application = ApplicationBuilder().token(BOT_TOKEN).build()
openai.api_key = OPENAI_API_KEY

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا رحيم 🤖 أقدر أجاوبك على أي سؤال 😊")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"📨 رسالة من {update.effective_user.first_name}: {user_message}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "حصل خطأ 😢، حاول تاني لاحقًا."
        print("❌ خطأ من OpenAI:", e)

    await update.message.reply_text(reply)

# إضافة الأوامر
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Webhook handler
async def webhook_handler(request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return web.Response(text="ok")

# إنشاء التطبيق AIOHTTP
web_app = web.Application()
web_app.router.add_post("/webhook", webhook_handler)

# تشغيل الخادم
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Bot running on port {port} ...")
    web.run_app(web_app, port=port)
