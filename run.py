import threading
import asyncio
from keep_alive import app, application

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# شغل Flask في خلفية
threading.Thread(target=run_flask).start()

# شغل البوت
async def run_bot():
    await application.initialize()
    await application.start()
    # نخلي البوت ينتظر التحديثات اللي بتيجي من التليقرام
    await application.updater.start_polling()
    await application.updater.idle()

asyncio.run(run_bot())
