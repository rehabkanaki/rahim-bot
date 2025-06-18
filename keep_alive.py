import os
import asyncio
from flask import Flask, request
from telegram import Update
from main import get_application

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
application = get_application()

@app.route('/')
def home():
    return "Bot is running ✅", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    print(f"📥 New update received: {update}")

    # نستخدم create_task لمعالجة التحديث في الخلفية
    asyncio.create_task(application.process_update(update))

    return "ok", 200
