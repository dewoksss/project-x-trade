@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Menangkap semua kemungkinan sumber data
    data_json = request.get_json(silent=True)
    data_form = request.form.to_dict()
    data_args = request.args.to_dict() # Ini menangkap data di URL (query params)
    data_raw = request.get_data(as_text=True)

    print("--- DETEKTIF WEHOOK AKTIF ---")
    print(f"JSON Body: {data_json}")
    print(f"Form Data: {data_form}")
    print(f"Query Args (URL): {data_args}")
    print(f"Raw Data: {data_raw}")
    print("--- SELESAI ---")

    return "OK", 200