import os
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
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "ok", 200
