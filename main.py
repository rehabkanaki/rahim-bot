import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ----------------------------
# إعدادات البوت
# ----------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")  # الأفضل تخزينه كمتغير بيئي
WEBHOOK_URL = f"https://your-app-name.onrender.com/{BOT_TOKEN}"

app = Flask(__name__)

application = Application.builder().token(BOT_TOKEN).build()

# ----------------------------
# أوامر البوت
# ----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك! 🌟 أنا شغال 24/7 مع Render.")

application.add_handler(CommandHandler("start", start))

# ----------------------------
# نقطة استقبال Webhook من Telegram
# ----------------------------

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        loop.close()

        return "ok"

# ----------------------------
# نقطة الفحص البسيط
# ----------------------------

@app.route("/")
def home():
    return "بوت رحيم شغال ✅"

# ----------------------------
# تشغيل Flask (للتجربة محلياً)
# ----------------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)
