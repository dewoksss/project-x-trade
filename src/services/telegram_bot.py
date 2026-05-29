import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Pastikan nama fungsi ini persis sama
def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("🚨 Error: Telegram Token atau Chat ID tidak ditemukan!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"🚨 Error Telegram: {e}")