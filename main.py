import os
import asyncio
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
    app = request.app["bot_app"]
    data = await request.json()
    update = Update.de_json(data, app.bot.token)
    await app.update_queue.put(update)
    return web.Response(text="ok")

async def init_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await app.initialize()
    await app.start()

    web_app = web.Application()
    web_app["bot_app"] = app
    web_app.router.add_post("/webhook", handle)

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"🚀 Bot is up and running on port {PORT}")
    
    # Keep running until terminated
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(init_app())
