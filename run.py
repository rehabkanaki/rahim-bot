import threading
import asyncio
from keep_alive import app, application

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# تشغيل Flask في خلفية
threading.Thread(target=run_flask).start()

# تشغيل بوت التليقرام
async def main():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # احتياطًا للتأكد من الاتصال

asyncio.run(main())
