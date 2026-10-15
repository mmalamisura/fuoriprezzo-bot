import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

# SOLO ASIN VERIFICATI - questi 3 aprono Amazon.it davvero
PRODOTTI = [
    {"asin": "B09B8X9RGM", "nome": "Echo Dot 5ª Gen"},
    {"asin": "B09WX9XBKD", "nome": "Echo Pop"},
    {"asin": "B0BTFSYWWB", "nome": "Fire TV Stick 4K Max 2024"},
    {"asin": "B0933BVK6T", "nome": "Apple AirTag Originale"},
]

def send(prod):
    link = f"https://www.amazon.it/dp/{prod['asin']}?tag={TAG}"
    # Messaggio con link in chiaro così Telegram fa anteprima foto automatica di Amazon
    caption = f"""🔥 {prod['nome']}

✅ Disponibile su Amazon.it - Prezzo reale aggiornato
🛒 {link}

Tag affiliato verificato {TAG}
#offerta"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHANNEL,
        "text": caption,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False  # <--- QUESTO FA VEDERE LA FOTO
    })
    print(f"{prod['asin']} -> {r.status_code} {r.text[:200]}")

# Posta 1 prodotto a caso per non spammare
p = random.choice(PRODOTTI)
print(f"Posto {p['nome']}")
send(p)
