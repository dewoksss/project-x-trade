import os
import time
import threading
import requests
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request
from src.database import init_db, save_order_to_db, get_order_by_id, update_order_status
from src.services.telegram_bot import send_telegram_alert
from src.services.discord_bot import send_discord_alert
from src.google_sheets import update_google_sheet

load_dotenv()
app = Flask(__name__)

# --- 1. Jalur Webhook (Terima notifikasi instan) ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"✅ Webhook diterima: {data}")
    return "OK", 200

def run_flask():
    app.run(port=5000, use_reloader=False)

# --- 2. Jalur Polling (Backup jika Webhook gagal) ---
def fetch_orders():
    url = f"{os.getenv('U7BUY_BASE_URL')}/orders"
    params = {
        "app_key": os.getenv('U7BUY_API_KEY'),
        "app_secret": os.getenv('U7BUY_APP_SECRET')
    }
    try:
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Error API: {e}")
        return None

def check_new_orders():
    orders_data = fetch_orders()
    
    # PERBAIKAN: Cek apakah data benar-benar ada sebelum diproses
    if orders_data is None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ API belum merespon atau akses ditolak (401).")
        return
        
    # Cek struktur JSON untuk memastikan ada key 'data' dan isinya list
    if 'data' not in orders_data or orders_data['data'] is None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ Tidak ada order baru.")
        return
    
    # Jika lolos pengecekan di atas, baru lakukan looping
    orders = orders_data['data']
    for order in orders:
        order_id = str(order.get('order_id'))
        status = order.get('status')
        # Lanjutkan logika proses order kamu di sini...
        print(f"✅ Memproses order: {order_id} - Status: {status}")

# --- 3. Eksekusi Utama ---
if __name__ == "__main__":
    print("=== PROJECT X-TRADE MEGA-ENGINE ACTIVE ===")
    init_db()

    # Jalankan Webhook di background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Loop utama untuk Polling
    while True:
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Memantau pesanan...")
            check_new_orders()
            time.sleep(60) 
        except KeyboardInterrupt:
            break