import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, Dispatcher, ContextTypes
from main import get_application  # نستورد التطبيق من main

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
application = get_application()  # نحصل على التطبيق من main
dispatcher: Dispatcher = application.dispatcher


@app.route('/')
def home():
    return "Bot is running ✅", 200


@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), application.bot)
    await dispatcher.process_update(update)
    return "ok", 200
