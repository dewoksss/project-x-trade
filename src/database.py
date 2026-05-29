import os
from dotenv import load_dotenv
from supabase import create_client

# Ambil langsung dari environment
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Debugging: Print nilai (ini akan muncul di log Railway)
print(f"DEBUG: URL terbaca: {supabase_url}")
print(f"DEBUG: KEY terbaca: {'[TERISI]' if supabase_key else '[KOSONG]'}")

if not supabase_url:
    raise ValueError("ERROR: SUPABASE_URL tidak ditemukan di environment variables!")

supabase = create_client(supabase_url, supabase_key)

# Inisialisasi client
supabase: Client = create_client(supabase_url, supabase_key)



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
        # Mengambil data dari tabel 'orders'
        response = supabase.table("orders").select("price").execute()
        # Jika ada data, jumlahkan harganya
        if response.data:
            total = sum(item['price'] for item in response.data)
            return total
        return 0
    except Exception as e:
        print(f"Error mengambil data cuan: {e}")
        return 0