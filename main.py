import requests, re, os, random, time
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept-Language": "it-IT,it;q=0.9",
    "Accept": "text/html,application/xhtml+xml"
}

PRODOTTI = [
    {"asin": "B09B8V1LZ3", "nome": "Echo Dot 5a gen", "idealo": 64.90},
    {"asin": "B0BP9SNVH6", "nome": "Fire TV Stick 4K", "idealo": 69.99},
    {"asin": "B0C7N5R6R6", "nome": "Echo Pop", "idealo": 39.99},
]

def get_price(asin):
    # Metodo 1: via proxy gratuito per evitare blocco Amazon
    try:
        amazon_url = f"https://www.amazon.it/dp/{asin}"
        proxy_url = f"https://api.allorigins.win/raw?url={amazon_url}"
        r = requests.get(proxy_url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        # cerca € xx,xx
        matches = re.findall(r"€\s*(\d+[,\.]\d+)", text)
        for m in matches:
            val = float(m.replace(",","."))
            if 10 < val < 1000:  # prezzo plausibile
                return val
    except Exception as e:
        print(f"Errore proxy {asin}: {e}")
    return None

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown"})

# TEST FORZATO - posta comunque il prezzo vero per vedere se funziona
for p in PRODOTTI:
    time.sleep(1)
    prezzo = get_price(p["asin"])
    print(f"Check {p['nome']}: Amazon {prezzo} vs Idealo {p['idealo']}")
    if prezzo:
        link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"
        msg = f"""🧪 *TEST BOT VERO* 

🎧 *{p['nome']}*
💰 Prezzo VERO letto ora: *{prezzo}€*
(Idealo media: {p['idealo']}€)

👉 [VAI SU AMAZON]({link})

Se vedi questo, il bot funziona e non inventa più 42€"""
        send(msg)
        print("POSTATO TEST!")
        break
else:
    print("Ancora bloccato - riprovo")
