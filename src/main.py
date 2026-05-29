import os
import time
import threading
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from src.database import init_db, save_order_to_db, get_order_by_id, update_order_status, supabase
from src.services.telegram_bot import send_telegram_alert
from src.services.discord_bot import send_discord_alert
from src.google_sheets import update_google_sheet

app = Flask(__name__)

# --- CONFIG ---
U7BUY_BASE_URL = os.getenv('U7BUY_BASE_URL', 'https://openapi.u7buy.com/prod-api')
U7BUY_API_KEY = os.getenv('U7BUY_API_KEY')
U7BUY_APP_SECRET = os.getenv('U7BUY_APP_SECRET')

# --- 1. Jalur Webhook (Paten agar tidak 'faulty') ---
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # 1. Respon instan untuk GET (Verifikasi)
    if request.method == 'GET':
        return "Webhook is active", 200
    
    # 2. Ambil data dalam bentuk apa pun agar tidak error
    try:
        data = request.get_json(silent=True) # Pakai silent=True agar tidak error
        if data is None:
            data = request.form.to_dict() # Coba ambil dari form-data jika bukan JSON
        
        print(f"✅ Webhook diterima: {data}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"❌ Error memproses webhook: {e}")
        return jsonify({"status": "error"}), 400

def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

# --- 2. Jalur Polling ---
def fetch_orders():
    url = f"{U7BUY_BASE_URL}/orders"
    params = {
        "app_key": U7BUY_API_KEY,
        "app_secret": U7BUY_APP_SECRET
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Error API: {e}")
        return None

def check_new_orders():
    orders_data = fetch_orders()
    if orders_data and 'data' in orders_data and orders_data['data']:
        for order in orders_data['data']:
            print(f"✅ Memproses order: {order.get('order_id')}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ Tidak ada order baru.")

# --- 3. Eksekusi Utama ---
if __name__ == "__main__":
    print("=== PROJECT X-TRADE MEGA-ENGINE ACTIVE ===")
    init_db()

    threading.Thread(target=run_flask, daemon=True).start()

    while True:
        try:
            check_new_orders()
            time.sleep(60) 
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(60)