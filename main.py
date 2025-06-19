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

# ========== المتغيرات ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثال: https://rahim-bot.onrender.com
openai.api_key = os.getenv("OPENAI_API_KEY")

# ========== إعداد التطبيق ==========
application = Application.builder().token(BOT_TOKEN).build()

# ========== دالة start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بيك! أنا رحيم، كيف أقدر أساعدك؟ 😊")

# ========== دالة الرد باستخدام OpenAI ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("حصل خطأ، حاول مرة تانية.")

# ========== إضافة الهاندلرز ==========
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ========== aiohttp webhook ==========
async def webhook_handler(request):
    if request.method == "POST":
        try:
            data = await request.json()
            update = Update.de_json(data, application.bot)
            await application.process_update(update)
        except Exception as e:
            print("Webhook error:", e)
        return web.Response()
    else:
        return web.Response(status=405)

async def start_webhook():
    # تهيئة التطبيق مرة واحدة فقط
    await application.initialize()
    await application.start()

    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)

    print("🚀 Rahim Bot is running via Webhook!")
    return app

# ========== تشغيل السيرفر ==========
if __name__ == "__main__":
    web.run_app(start_webhook(), port=int(os.environ.get("PORT", 10000)))
