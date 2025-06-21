import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات اللوق
logging.basicConfig(level=logging.INFO)

# المتغيرات
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL", "").rstrip("/")  # يشيل أي / في الآخر
PORT = int(os.environ.get("PORT", 10000))

# عرّفي رابط الويب هوك هنا
webhook_url = f"{APP_URL}/webhook"

# دوال البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 البوت شغال على Render بدون Flask!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message and update.message.text:
            logging.info(f"📨 استلمت رسالة: {update.message.text}")
            await update.message.reply_text(f"📨 وصلتني: {update.message.text}")
        else:
            logging.info("⚠ استلمت رسالة لكنها ليست نصية.")
            await update.message.reply_text("❗ المعذرة، الرسالة غير نصية.")
    except Exception:
        logging.exception("حصل خطأ في handle_message")
        await update.message.reply_text("❌ حصل خطأ أثناء معالجة الرسالة.")

# تشغيل البوت
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        stop_signals=None
    )
