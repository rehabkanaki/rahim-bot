import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")  # أو اكتبي التوكن مباشرة
APP_URL = os.getenv("APP_URL")  # أو اكتبي الرابط مباشرة، بدون سلاش في الآخر

# مثال مباشر لو ما دايرة تستخدمي os.getenv
# BOT_TOKEN = "123456:ABC..."
# APP_URL = "https://rahim-bot.onrender.com"

webhook_url = f"{APP_URL}/{BOT_TOKEN}"

res = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": webhook_url}
)

print(res.status_code, res.text)
