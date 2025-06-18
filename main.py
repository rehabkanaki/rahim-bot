import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

# جملتك الشهيرة لما نزور الرابط
async def home(request):
    return "Rahim شغال ✅"

# توكن البوت والرابط الخارجي
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثلاً: https://rahim-bot.onrender.com

# بوت البداية
app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً، أنا بوت رحيم 🧠💬")

app_bot.add_handler(CommandHandler("start", start))

# تفعيل الـ webhook إذا APP_URL موجود
async def set_webhook():
    if APP_URL:
        await app_bot.bot.set_webhook(f"{APP_URL}/{TELEGRAM_TOKEN}")
        print("✅ Webhook set")
    else:
        print("⚠️ APP_URL not set, using long polling")

# تشغيل البوت
async def run_bot():
    await set_webhook()
    if APP_URL:
        # تشغيل ويب هوك
        await app_bot.run_webhook(
            listen="0.0.0.0",
            port=10000,
            webhook_url=f"{APP_URL}/{TELEGRAM_TOKEN}",
        )
    else:
        # تشغيل polling من اللابتوب
        await app_bot.run_polling()

if __name__ == "__main__":
    asyncio.run(run_bot())
