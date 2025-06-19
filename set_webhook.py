import os
import requests

# جلب التوكن والرابط من متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثال: https://rahim-bot.onrender.com

# التحقق من القيم
if not BOT_TOKEN or not APP_URL:
    raise ValueError("❌ تأكد من أن متغيرات البيئة BOT_TOKEN و APP_URL معرفة.")

# تحديد رابط الويب هوك (مفضل استخدام مسار ثابت مثل /webhook)
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{APP_URL}{WEBHOOK_PATH}"

# إرسال طلب لتعيين الويب هوك
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)

# طباعة النتيجة
if response.status_code == 200:
    print("✅ تم تعيين الـ Webhook بنجاح.")
else:
    print("❌ فشل في تعيين الـ Webhook:")
    print(response.status_code, response.text)
