from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # 1. Catat semua informasi request yang masuk
    print("--- MULAI MENERIMA REQUEST ---")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body: {request.get_data(as_text=True)}") # Mengambil mentah-mentah apa pun yang dikirim
    print("--- SELESAI ---")

    # 2. Kirim respon standar yang paling aman
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)