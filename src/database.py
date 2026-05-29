import os
from dotenv import load_dotenv
from supabase import create_client

# Load konfigurasi
load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

# Inisialisasi client
supabase = create_client(supabase_url, supabase_key)



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