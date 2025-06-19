import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 8443))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! بوت رحيم شغال ✅")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 رسالة جديدة وصلت:", update.message.text)
    await update.message.reply_text(f"إنت كتبت: {update.message.text}")

async def handle(request):
    # تهيئة التطبيق
    app = request.app["bot_app"]
    update = Update.de_json(await request.json(), app.bot.token)
    await app.update_queue.put(update)
    return web.Response(text="ok")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    web_app = web.Application()
    web_app["bot_app"] = app
    web_app.router.add_post("/webhook", handle)

    # شغل التطبيق والـ webhook مع aiohttp
    app.start()
    web.run_app(web_app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
