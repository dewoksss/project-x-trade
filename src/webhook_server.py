from flask import Flask, request, jsonify
from database import save_order_to_db # Mengambil fungsi dari file database.py

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Log data untuk keperluan observasi riset (nanti bisa dimasukkan ke laporan)
    print(f"DEBUG: Menerima data dari U7BUY: {data}")
    
    # Simpan ke Supabase (sesuaikan key di bawah dengan JSON dari U7BUY)
    save_order_to_db(data['order_id'], data['item'], data['qty'], data['price'], data['status'])
    
    return jsonify({"status": "success"}), 200