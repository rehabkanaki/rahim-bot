import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL", "").rstrip("/")  # Remove trailing slash
PORT = int(os.environ.get("PORT", 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 البوت شغال على Render بدون Flask!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message and update.message.text:
            await update.message.reply_text(f"📨 وصلتني: {update.message.text}")
        else:
            await update.message.reply_text("❗ المعذرة، الرسالة غير نصية.")
    except Exception as e:
        logging.exception("حصل خطأ في handle_message")
        await update.message.reply_text("❌ حصل خطأ أثناء معالجة الرسالة.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{APP_URL}/{BOT_TOKEN}"
        stop_signals=None  # يمنع البوت يقفل من تلقاء نفسه
)

    )
