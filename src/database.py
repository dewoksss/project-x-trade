import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env (hanya berpengaruh saat dijalankan lokal di laptop)
load_dotenv()

# Gunakan URL yang sudah pasti (hardcoded) untuk menghindari error 'None' di Railway
# Jika nanti URL Supabase berubah, cukup ganti di baris bawah ini
SUPABASE_URL = "https://jbasqjpwzvybhuzvihag.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debugging untuk memastikan di log Railway
print(f"DEBUG: URL yang digunakan: {SUPABASE_URL}")
print(f"DEBUG: KEY terbaca: {'[TERISI]' if SUPABASE_KEY else '[KOSONG]'}")

if not SUPABASE_KEY:
    raise ValueError("ERROR: SUPABASE_KEY tidak ditemukan di environment variables!")

# Inisialisasi client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    print("Inisialisasi database berhasil.")

def get_order_by_id(order_id):
    try:
        response = supabase.table("orders").select("*").eq("order_id", order_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error mencari order: {e}")
        return None

def update_order_status(order_id, new_status):
    try:
        supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()
    except Exception as e:
        print(f"Error update status: {e}")

def save_order_to_db(order_id, item, qty, price, status):
    try:
        data = {
            "order_id": order_id,
            "item": item,
            "qty": qty,
            "price": price,
            "status": status
        }
        response = supabase.table("orders").insert(data).execute()
        return response
    except Exception as e:
        print(f"Error menyimpan ke database: {e}")
        return None

def get_total_cuan():
    try:
        response = supabase.table("orders").select("price").execute()
        if response.data:
            total = sum(item['price'] for item in response.data)
            return total
        return 0
    except Exception as e:
        print(f"Error mengambil data cuan: {e}")
        return 0