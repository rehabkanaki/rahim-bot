import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثل: https://rahim-bot.onrender.com

webhook_url = f"{APP_URL}/webhook"

res = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": webhook_url}
)

print(res.status_code, res.text)
