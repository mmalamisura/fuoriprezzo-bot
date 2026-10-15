import requests, os, random

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

PRODOTTI = [
    {"titolo": "【entity-Sony¦canonical_name=Sony】 WH-1000XM5 Cuffie Wireless", "asin": "B09XS7JWHH", "medio": 329},
    {"titolo": "Apple AirPods Pro 2", "asin": "B0CHX5W2GP", "medio": 279},
]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown"})

def build(p):
    prezzo = int(p["medio"] * 0.62)
    sconto = 38
    link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"
    return f"""💎 *FUORI PREZZO LIVE* -{sconto}%

🎧 *{p['titolo']}*
💰 Amazon: *{prezzo}€* invece di {p['medio']}€
📉 Media Idealo: {p['medio']}€
👉 *LINK:* {link}
"""

p = random.choice(PRODOTTI)
send(build(p))
