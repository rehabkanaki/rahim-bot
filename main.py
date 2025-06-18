import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! بوت رحيم شغال ✅")

# الرد التلقائي على أي رسالة
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"إنت كتبت: {user_message}")

# نبني التطبيق (exported function)
def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    return app


if __name__ == "__main__":
    from keep_alive import app as flask_app
    import asyncio
    import threading

    def run_flask():
        flask_app.run(host="0.0.0.0", port=10000)

    threading.Thread(target=run_flask).start()

    application = get_application()
    asyncio.run(application.initialize())
    asyncio.run(application.start())
    asyncio.get_event_loop().run_forever()
