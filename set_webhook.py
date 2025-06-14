import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثلاً: https://rahim-bot.onrender.com

webhook_url = f"{APP_URL}/{BOT_TOKEN}"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    data={"url": webhook_url}
)

print("Webhook set response:", response.json())
