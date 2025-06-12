import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# إعداد الـ Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إعداد مفتاح OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# دالة لمعالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي في مجموعة تليقرام."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()

        await update.message.reply_text(bot_reply)

    except Exception as e:
        logging.error(f"حدث خطأ: {e}")
        await update.message.reply_text("حدث خطأ أثناء الاتصال بـ OpenAI.")

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ البوت شغال...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
