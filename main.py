import requests, re, os
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get_amazon_price(asin):
    try:
        url = f"https://www.amazon.it/dp/{asin}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # cerca prezzo
        text = soup.get_text()
        m = re.search(r"(\d+,\d+)\s*€", text)
        if m:
            return float(m.group(1).replace(",","."))
    except Exception as e:
        print(e)
    return None

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": False})

# PRODOTTI con ASIN veri di Amazon.it
PRODOTTI = [
    {"asin": "B0C7N5R6R6", "nome": "Echo Dot 5", "idealo": 69},
    {"asin": "B0BFC8SBB3", "nome": "Fire TV Stick 4K Max", "idealo": 79},
]

for p in PRODOTTI:
    amazon = get_amazon_price(p["asin"])
    print(f"{p['nome']} Amazon: {amazon} vs Idealo {p['idealo']}")
    if amazon and amazon < p["idealo"] * 0.75:  # solo se -25% vero
        sconto = int(100 - (amazon*100/p["idealo"]))
        link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"
        msg = f"""💎 *FUORI PREZZO LIVE* -{sconto}%

🎧 *{p['nome']}*
💰 Amazon: *{amazon}€* invece di {p['idealo']}€
📉 Risparmi {p['idealo']-amazon:.0f}€

👉 [COMPRA SU AMAZON]({link})"""
        send(msg)
        break
else:
    print("Nessun fuori prezzo reale oggi - non posto nulla per non mentire")
