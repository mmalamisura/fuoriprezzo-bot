import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

# TUTTI VERIFICATI SU AMAZON.IT ORA
PRODOTTI = [
    {"asin": "B09B8X9RGM", "nome": "Echo Dot 5ª Gen"},
    {"asin": "B09WX9XBKD", "nome": "Echo Pop"},
    {"asin": "B0BTFSYWWB", "nome": "Fire TV Stick 4K Max 2024"},
    {"asin": "B09364K56M", "nome": "Apple AirTag (1 pezzo) Originale"},
    {"asin": "B0936LWNHQ", "nome": "Apple AirTag 4 pezzi Originali"},
]

def send(prod):
    link = f"https://www.amazon.it/dp/{prod['asin']}?tag={TAG}"
    # Link in chiaro su riga separata = Telegram fa anteprima foto automatica
    text = f"""🔥 {prod['nome']}

✅ Disponibile su Amazon.it
👇 Prezzo reale qui:

{link}

#offerta {TAG}"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHANNEL,
        "text": text,
        "disable_web_page_preview": False
    })
    print(f"{prod['asin']} -> {r.status_code}")

p = random.choice(PRODOTTI)
print(f"Posto {p['asin']}")
send(p)
