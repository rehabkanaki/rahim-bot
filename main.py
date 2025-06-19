import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! بوت رحيم شغال ✅")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 رسالة جديدة وصلت:", update.message.text)
    await update.message.reply_text(f"إنت كتبت: {update.message.text}")

def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return app

if __name__ == "__main__":
    app = get_application()
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=f"{APP_URL}/webhook",
        webhook_path="/webhook"  # مهم جداً عشان يشتغل Webhook صح
    )
