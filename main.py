import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

PRODOTTI = [
    {"asin": "B09B8V1LZ3", "nome": "Echo Dot 5ª Gen - Altoparlante Alexa"},
    {"asin": "B0BP9SNVH6", "nome": "Fire TV Stick 4K Max - Streaming"},
    {"asin": "B0C7N5R6R6", "nome": "Echo Pop - Compatto con Alexa"},
    {"asin": "B0C8MPM8Z9", "nome": "Sony WH-1000XM5 - Cuffie Noise Cancelling"},
    {"asin": "B0CCJTL8L1", "nome": "Apple AirTag - Tracker"},
]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown"})
    print(f"TELEGRAM RISPOSTA: {r.status_code} - {r.text[:200]}")

p = random.choice(PRODOTTI)
link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"

msg = f"""🔥 *{p['nome']}*

✅ Disponibile su Amazon.it
👉 Link affiliato verificato attivo

🛒 [VEDI PREZZO REALE SU AMAZON]({link})

I prezzi cambiano spesso, verifica al checkout.
#amazon #offerta #{p['asin'][:5]}"""

print(f"Sto postando {p['nome']} su {CHANNEL}")
send(msg)
