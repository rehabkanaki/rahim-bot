import threading
import asyncio
from keep_alive import app, application

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

asyncio.run(application.initialize())
asyncio.run(application.start())
asyncio.get_event_loop().run_forever()
