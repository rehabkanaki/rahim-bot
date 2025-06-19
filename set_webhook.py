import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

if not BOT_TOKEN or not APP_URL:
    raise ValueError("تأكد من تعريف BOT_TOKEN وAPP_URL في متغيرات البيئة")

WEBHOOK_URL = f"{APP_URL}/webhook"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)

if response.status_code == 200:
    print("✅ تم تعيين Webhook بنجاح")
else:
    print("❌ فشل تعيين Webhook:", response.status_code, response.text)
