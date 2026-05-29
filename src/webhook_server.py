from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    print("--- BERHASIL! U7BUY TERHUBUNG ---")
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)