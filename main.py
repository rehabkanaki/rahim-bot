import os
import openai
from aiohttp import web
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# المتغيرات من البيئة
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثال: https://rahim-bot.onrender.com
openai.api_key = os.getenv("OPENAI_API_KEY")

# =========================
# تهيئة التطبيق
# =========================
application = Application.builder().token(BOT_TOKEN).build()

# =========================
# أمر /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بيك! 👋 أنا رحيم، كيف أساعدك اليوم؟ 😇")

# =========================
# التعامل مع الرسائل
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        # طباعة تفاصيل الخطأ على السجل
        print(f"❌ OpenAI Error: {e}")

        # الرد على المستخدم
        await update.message.reply_text(
            "حصل خطأ من جهة الذكاء الاصطناعي، جرّب تاني بعد شوية."
        )

# =========================
# إضافة الهاندلرز
# =========================
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# =========================
# إعداد الويب هوك
# =========================
async def webhook_handler(request):
    """معالجة الطلبات القادمة من تليجرام عبر الويب هوك"""
    if request.method == "POST":
        try:
            data = await request.json()
            update = Update.de_json(data, application.bot)
            await application.process_update(update)
        except Exception as e:
            print(f"❌ Webhook error: {e}")

        return web.Response()
    else:
        return web.Response(status=405)

async def start_webhook():
    """تهيئة وتشغيل البوت على الويب هوك"""
    await application.initialize()
    await application.start()

    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)

    print(f"🚀 Rahim Bot is running via Webhook on {APP_URL}")
    return app

# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(start_webhook(), port=port)
