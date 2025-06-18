import threading
import asyncio
from keep_alive import app, application

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

async def start():
    await application.initialize()
    await application.start()
    print("🤖 Rahim bot is ready and listening...")

    # نخلي الـ event loop يشتغل للأبد
    await asyncio.Event().wait()

asyncio.run(start())

