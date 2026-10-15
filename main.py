import requests, os, random

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": False})

PRODOTTI = [
    {"titolo": "Echo Dot 5ª generazione", "asin": "B09B8VGCR8", "medio": 69},
    {"titolo": "Fire TV Stick 4K", "asin": "B0BP9SNVH6", "medio": 79},
    {"titolo": "Sony WH-1000XM5", "asin": "B09XS7JWHH", "medio": 329},
]

p = random.choice(PRODOTTI)
prezzo = int(p["medio"] * 0.62)
sconto = 38
link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"

msg = f"""💎 *FUORI PREZZO LIVE* -{sconto}%

🎧 *{p['titolo']}*
💰 Amazon: *{prezzo}€* invece di {p['medio']}€

👉 [COMPRA SU AMAZON]({link})

#offerta #amazon"""

send(msg)
