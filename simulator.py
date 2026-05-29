import os
import sys
import time
import random
import sqlite3
import datetime
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Muat variabel rahasia dari file .env
load_dotenv()

# === KONFIGURASI TELEGRAM & DISCORD ===
TELEGRAM_BOT_TOKEN = "8568041973:AAE1Z3HoKKrazDLYDfKYxyIsluNDr0fBIhM"
TELEGRAM_CHAT_ID = 1394373735
DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1508658006252851332/fourAJhIMciqBeSZbgLD3ql7-iE7yztbB-LZcbiodgzfdmCZP1mxo5SBRAmUgvFFtU7L"

# === DAFTAR ITEM GAME UNTUK SIMULASI (Mock Data) ===
MOCK_ITEMS = [
    {"name": "186.9T/s Bacon Mutation", "base_price_range": (15000.0, 25000.0)},
    {"name": "218.1T/s Volcanic Mutation", "base_price_range": (25000.0, 35000.0)},
    {"name": "218.1T/s Phantom Mutation", "base_price_range": (35000.0, 45000.0)},
    {"name": "186.9T/s Rainbow Mutation", "base_price_range": (40000.0, 55000.0)}
]

# === WARNA TERMINAL UNTUK CYBER EFFECT ===
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def inisialisasi_database_lokal():
    """Membuat database x_trade.db dan tabel transaksi jika belum ada"""
    print(f"{CYAN}[SYSTEM] Menginisialisasi database SQLite lokal...{RESET}")
    conn = sqlite3.connect('x_trade.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            nama_item TEXT,
            harga_jual REAL,
            fee REAL,
            modal REAL,
            cuan REAL,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"{GREEN}[SUCCESS] Database x_trade.db siap digunakan!{RESET}\n")

def kirim_notifikasi_telegram(item_name, harga_jual, fee, modal, cuan):
    """Mengirim pesan estetik ala struk belanja ke Telegram Bot"""
    if TELEGRAM_BOT_TOKEN in ["MASUKKAN_TOKEN_BOT_TELEGRAM_MU", None, ""]:
        print(f"{YELLOW}[WARN] Token Telegram belum diisi di .env. Notifikasi Telegram dilewati.{RESET}")
        return

    pesan = (
        "🔔 <b>[PROJECT X-TRADE] - TRANSAKSI BARU!</b> 🔔\n"
        "<code>==============================</code>\n"
        f"📦 <b>Item:</b> {item_name}\n"
        f"💰 <b>Harga Jual:</b> Rp {harga_jual:,.2f}\n"
        f"💸 <b>Fee Admin (10%):</b> Rp {fee:,.2f}\n"
        f"🧱 <b>Modal:</b> Rp {modal:,.2f}\n"
        "<code>------------------------------</code>\n"
        f"🟢 <b>EST. CUAN BERSIH:</b> <b>Rp {cuan:,.2f}</b>\n"
        "<code>==============================</code>\n"
        "🕒 Status: <i>SUCCESS (AUTO-LOGGED)</i>\n"
        "👤 Developer: Ariyan - UTB"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"{GREEN}[TELEGRAM] Notifikasi berhasil dikirim! TING! 🔔{RESET}")
        else:
            print(f"{RED}[TELEGRAM] Gagal mengirim pesan. Code: {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[TELEGRAM] Error koneksi: {e}{RESET}")

def kirim_notifikasi_discord(item_name, harga_jual, fee, modal, cuan):
    """Mengirim embed alert keren ke Discord via Webhook"""
    if not DISCORD_WEBHOOK:
        print(f"{YELLOW}[WARN] Discord Webhook URL belum diatur di .env. Notifikasi Discord dilewati.{RESET}")
        return

    payload = {
        "username": "Xushar Store Bot",
        "embeds": [
            {
                "title": "🔥 ADA PESANAN ROBLOX BARU! (SIMULASI) 🔥",
                "description": "Halo Bos, ada cuan masuk nih di toko U7BUY!",
                "color": 16743168,  # Warna Oranye (Hex: #FF6600)
                "fields": [
                    {"name": "📦 Item Name", "value": f"`{item_name}`", "inline": True},
                    {"name": "💰 Harga Jual", "value": f"`Rp {harga_jual:,.2f}`", "inline": True},
                    {"name": "💸 Est. Fee (10%)", "value": f"`Rp {fee:,.2f}`", "inline": True},
                    {"name": "🧱 Modal Item", "value": f"`Rp {modal:,.2f}`", "inline": True},
                    {"name": "🟢 Cuan Bersih", "value": f"`Rp {cuan:,.2f}`", "inline": False}
                ],
                "footer": {
                    "text": "Project X-Trade Automation Engine"
                },
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204:
            print(f"{GREEN}[DISCORD] Notifikasi sukses dikirim ke Discord! 📬{RESET}")
        else:
            print(f"{RED}[DISCORD] Gagal mengirim ke Discord. Code: {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[DISCORD] Error Webhook Discord: {e}{RESET}")

def simpan_ke_database(tanggal, item_name, harga_jual, fee, modal, cuan):
    """Menyimpan data transaksi ke database SQLite lokal"""
    try:
        conn = sqlite3.connect('x_trade.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transaksi (tanggal, nama_item, harga_jual, fee, modal, cuan, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tanggal, item_name, harga_jual, fee, modal, cuan, 'Sukses'))
        conn.commit()
        conn.close()
        print(f"{GREEN}[SQLITE] Transaksi sukses dikunci di x_trade.db!{RESET}")
    except Exception as e:
        print(f"{RED}[SQLITE] Gagal menyimpan data: {e}{RESET}")

def kirim_ke_google_sheets(tanggal, item_name, harga_jual, modal):
    """Menyinkronkan data transaksi dengan rumus dinamis ke Google Sheets"""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("xtrade-project").sheet1

        # Hitung baris berikutnya secara otomatis
        baris_target = len(sheet.get_all_values()) + 1
        
        # Meracik formula dinamis agar rumus di Sheets kamu tidak ketimpa
        rumus_fee = f"=C{baris_target}*10%"
        rumus_cuan = f"=C{baris_target}-D{baris_target}-E{baris_target}"

        data_fix = [
            [tanggal, item_name, harga_jual, rumus_fee, modal, rumus_cuan, "Sukses"]
        ]
        
        # Kunci kolom A sampai G di baris target
        rentang_target = f"A{baris_target}:G{baris_target}"
        sheet.update(range_name=rentang_target, values=data_fix, value_input_option='USER_ENTERED')
        print(f"{GREEN}[SHEETS] Cloud Spreadsheet 'xtrade-project' berhasil tersinkronisasi otomatis!{RESET}")
    except Exception as e:
        print(f"{RED}[SHEETS] Gagal menyinkronkan ke Google Sheets: {e}{RESET}")

def jalankan_simulator():
    """Loop utama untuk menjalankan simulasi orderan masuk"""
    print(f"{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}{CYAN}       WELCOME TO PROJECT X-TRADE FULL SIMULATOR     {RESET}")
    print(f"{BOLD}{CYAN}===================================================={RESET}")
    print(f"Developer: Ariyan Kusharthantho (UTB)")
    print(f"Simulator berjalan setiap 15-30 detik secara acak.")
    print("Tekan Ctrl+C untuk menghentikan simulasi.\n")

    inisialisasi_database_lokal()

    order_count = 0
    try:
        while True:
            order_count += 1
            print(f"\n{YELLOW}[WAIT] Mencari orderan baru di marketplace...{RESET}")
            
            # Waktu tunggu simulasi acak antara 15 sampai 30 detik
            delay = random.randint(15, 30)
            time.sleep(delay)

            # Pilih item dan kalkulasi cuan secara acak
            item = random.choice(MOCK_ITEMS)
            item_name = item["name"]
            harga_jual = round(random.uniform(item["base_price_range"][0], item["base_price_range"][1]), 4)
            
            # LOGIKA MATEMATIKA CUAN
            fee = round(harga_jual * 0.10, 4)
            modal = round(random.uniform(500.0, 3000.0), 4)
            cuan = round(harga_jual - fee - modal, 4)
            tanggal_sekarang = datetime.datetime.now().strftime("%Y-%m-%d")

            print(f"\n{BOLD}{GREEN}⚡ [ORDER MASUK #{order_count}] {item_name} terjual seharga Rp {harga_jual:,.2f}!{RESET}")
            
            # Jalankan Seluruh Pilar Otomatisasi X-Trade secara berurutan
            simpan_ke_database(tanggal_sekarang, item_name, harga_jual, fee, modal, cuan)
            kirim_ke_google_sheets(tanggal_sekarang, item_name, harga_jual, modal)
            kirim_notifikasi_telegram(item_name, harga_jual, fee, modal, cuan)
            kirim_notifikasi_discord(item_name, harga_jual, fee, modal, cuan)

    except KeyboardInterrupt:
        print(f"\n\n{RED}[SYSTEM] Simulator dihentikan oleh pengguna. Sampai jumpa, Yan!{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    jalankan_simulator()