import datetime
import os
import sqlite3
import gspread
from dotenv import load_dotenv
import requests
from oauth2client.service_account import ServiceAccountCredentials

# Muat variabel rahasia dari file .env
load_dotenv()
TM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def kirim_notif_telegram(nama_item, harga_jual, modal, fee, cuan):
    """Fungsi sakti buat ngirim laporan cuan estetik ke HP kamu"""
    if not TM_TOKEN or not TM_CHAT_ID:
        print("⚠️ Notif Telegram dilewati karena Token/Chat ID di .env belum diisi.")
        return

    pesan = (
        "🔔 *PROJECT X-TRADE: ORDERAN MASUK!* 🔔\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
         f"📦 *Item:* {nama_item}\n"
         f"💰 *Harga Jual:* Rp {harga_jual:,.2f}\n"
         f"💸 *Est. Fee (10%):* Rp {fee:,.2f}\n"
         f"📉 *Modal:* Rp {modal:,.2f}\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
         f"🔥 *CUAN BERSIH:* Rp {cuan:,.2f} 🔥\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Status: *Sukses Tercatat di Sistem!* 🚀"
    )

    url = f"https://api.telegram.org/bot{TM_TOKEN}/sendMessage"
    payload = {"chat_id": TM_CHAT_ID, "text": pesan, "parse_mode": "Markdown"}

    try:
        requests.post(url, json=payload)
        print("🔔 [TELEGRAM] Notifikasi cuan berhasil dikirim ke HP-mu!")
    except Exception as e:
        print(f"⚠️ Gagal kirim notif Telegram: {e}")


def sistem_pencatatan_terintegrasi(nama_item, harga_jual, modal_item):
    print("\n==================================================")
    print("🚀 MEMULAI SISTEM INTEGRASI: DB -> SHEETS -> TELEGRAM")
    print("==================================================")

    # Hitung matematika dasar di Python buat keperluan DB & Telegram
    est_fee = harga_jual * 0.10
    cuan_bersih = harga_jual - est_fee - modal_item
    tanggal_sekarang = datetime.date.today().strftime("%Y-%m-%d")

    # -----------------------------------------------------------------
    # KULIKAN 1: SIMPAN KE DATABASE LOKAL (x_trade.db)
    # -----------------------------------------------------------------
    try:
        print("🗄️  [DB LOKAL] Menghubungkan ke x_trade.db...")
        conn = sqlite3.connect("x_trade.db")
        cursor = conn.cursor()

        # Bikin tabel otomatis kalau belum ada
        cursor.execute(
            """
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
        """
        )

        # Suntik data ke database lokal
        cursor.execute(
            """
            INSERT INTO transaksi (tanggal, nama_item, harga_jual, fee, modal, cuan, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (tanggal_sekarang, nama_item, harga_jual, est_fee, modal_item, cuan_bersih, "Sukses"),
        )
        conn.commit()
        conn.close()
        print("✅ [DB LOKAL] Sukses mengunci data di komputer lokal!")
    except Exception as e:
        print(f"❌ [DB LOKAL] Gagal menyimpan: {e}")

    # -----------------------------------------------------------------
    # KULIKAN 2: SINKRONISASI KE GOOGLE SHEETS CLOUD
    # -----------------------------------------------------------------
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("xtrade-project").sheet1

        baris_target = len(sheet.get_all_values()) + 1
        rumus_fee = f"=C{baris_target}*10%"
        rumus_cuan = f"=C{baris_target}-D{baris_target}-E{baris_target}"

        data_fix = [[tanggal_sekarang, nama_item, harga_jual, rumus_fee, modal_item, rumus_cuan, "Sukses"]]
        rentang_target = f"A{baris_target}:G{baris_target}"

        sheet.update(range_name=rentang_target, values=data_fix, value_input_option="USER_ENTERED")
        print("✅ [CLOUD SHEETS] Data dan rumus mendarat aman di spreadsheet!")
    except Exception as e:
        print(f"❌ [CLOUD SHEETS] Gagal sinkronisasi: {e}")

    # -----------------------------------------------------------------
    # KULIKAN 3: KIRIM BROADCST NOTIFIKASI TELEGRAM
    # -----------------------------------------------------------------
    kirim_notif_telegram(nama_item, harga_jual, modal_item, est_fee, cuan_bersih)
    print("==================================================\n")


# --- TES AMUNISI FULL POWER ---
# Kita coba simulasikan orderan fiktif bernilai tinggi dengan desimal presisi!
sistem_pencatatan_terintegrasi("186.9T/s Bacon Mutation", 22569.7956, 2000)