import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Memastikan environment variable terbaca
load_dotenv()

def send_discord_alert(order_id, item_name, qty, alert_type="NEW_ORDER"):
    """Mengirim berbagai jenis notifikasi ke Discord"""
    
    # Mengambil URL webhook secara dinamis dari file .env
    DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

    # Pencegahan jika webhook belum diisi
    if not DISCORD_WEBHOOK or DISCORD_WEBHOOK == "None":
        print("🚨 Error: DISCORD_WEBHOOK_URL tidak ditemukan di file .env!")
        return

    # Logika pemilihan pesan
    if alert_type == "NEW_ORDER":
        title = "🔥 ADA PESANAN ROBLOX BARU! 🔥"
        color = 16743168
        desc = "Halo Bos, ada cuan masuk nih!"
        mention = ""
    elif alert_type == "REMINDER":
        title = "🚨 REMINDER: ORDERAN BELUM DIPROSES! 🚨"
        color = 16515840
        desc = "Woi Bos! Orderan ini udah kelamaan dicuekin!"
        mention = "@everyone "
    else:
        title = "Info"
        color = 16777215
        desc = "Notifikasi sistem"
        mention = ""

    payload = {
        "content": mention,
        "username": "Project X-Trade System",
        "embeds": [
            {
                "title": title,
                "description": desc,
                "color": color,
                "fields": [
                    {"name": "📦 Item Name", "value": f"`{item_name}`", "inline": True},
                    {"name": "🔢 Quantity", "value": f"`{qty}`", "inline": True},
                    {"name": "🆔 Order ID", "value": f"`{order_id}`", "inline": False}
                ],
                "footer": {"text": "Project X-Trade Automation Engine"},
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        ]
    }
    
    # Eksekusi kirim ke Discord
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        response.raise_for_status() # Akan memunculkan error jika request gagal
    except Exception as e:
        print(f"🚨 Error Webhook Discord: {e}")