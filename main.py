import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# قراءة المتغيرات من بيئة Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")  # مثال: https://rahim-bot.onrender.com

app = Flask(__name__)

# إنشاء التطبيق
application = Application.builder().token(BOT_TOKEN).build()


# ===== تعريف الأوامر =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 مرحبًا! البوت جاهز للعمل على Render ✅")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f"📨 وصلتني رسالتك: {text}")


# ===== إعداد الحدث =====
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


# ===== مسار الويب هوك =====
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """نقطة الدخول لاستقبال التحديثات من تليقرام"""
    data = request.get_json()
    update = Update.de_json(data, application.bot)
    application.update_queue.put(update)
    return "OK"

@app.route("/")
def index():
    """للتحقق من عمل الخدمة"""
    return "Bot is running ✅"


if __name__ == "__main__":
    # إعداد الويب هوك عند تشغيل الملف محليًا
    if APP_URL:
        async def set_webhook():
            await application.bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")

        import asyncio
        asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
