@app.route('/webhook', methods=['POST'])
def webhook():
    # Coba ambil JSON, jika gagal ambil form data, jika gagal ambil data mentah
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict() # Ambil jika formatnya form
        if not data:
            data = request.get_data(as_text=True) # Ambil teks mentah sebagai upaya terakhir
    
    print(f"DEBUG - Data yang diterima: {data}")
    
    # Berikan respon 200 agar U7BUY senang
    return jsonify({"status": "received", "data": str(data)}), 200