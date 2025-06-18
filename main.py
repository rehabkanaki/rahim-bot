import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! بوت رحيم شغال ✅")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 رسالة جديدة وصلت:", update.message.text)  # طباعة للتأكد
    await update.message.reply_text(f"إنت كتبت: {update.message.text}")

def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return app
