import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

# SOLO PRODOTTI DISPONIBILI CON CARRELLO SU 【entity-AMAZON¦canonical_name=Amazon】.IT
PRODOTTI = [
    {"asin": "B09B8X9RGM", "nome": "Echo Dot 5ª Gen - Alexa"},
    {"asin": "B09WX9XBKD", "nome": "Echo Pop - Smart Speaker"},
    {"asin": "B0BTFSYWWB", "nome": "Fire TV Stick 4K Max 2024"},
    {"asin": "B0GJTFY58R", "nome": "【entity-Apple¦canonical_name=Apple】 AirTag 2ª Gen 2025 - NUOVO"},
]

def send(prod):
    link = f"https://www.amazon.it/dp/{prod['asin']}?tag={TAG}"
    text = f"""🔥 {prod['nome']}

✅ Disponibile ora su 【entity-Amazon¦canonical_name=Amazon】.it
Con carrello e Prime

👇 Prezzo reale e acquisto:

{link}

#offerta"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHANNEL,
        "text": text,
        "disable_web_page_preview": False
    })
    print(f"{prod['asin']} -> {r.status_code} {r.text[:200]}")

p = random.choice(PRODOTTI)
print(f"Posto {p['asin']} - {p['nome']}")
send(p)
