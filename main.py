import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"
def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": False})
p = {"titolo": "Echo Dot 5a", "asin": "B09B8VGCR8", "medio": 69}
link = f"https://www.amazon.it/dp/{p['asin']}/?tag={TAG}"
msg = f"""💎 FUORI PREZZO LIVE -38%

🎧 {p['titolo']}
💰 Amazon: 42€ invece di 69€

👉 [COMPRA SU AMAZON]({link})

#offerta #amazon"""
send(msg)
