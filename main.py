import requests, re, os, random, time
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "it-IT,it;q=0.9"
}

PRODOTTI = [
    {"asin": "B09B8V1LZ3", "nome": "Echo Dot 5a gen", "idealo": 64.90},
    {"asin": "B0BP9SNVH6", "nome": "Fire TV Stick 4K", "idealo": 69.99},
    {"asin": "B0C7N5R6R6", "nome": "Echo Pop", "idealo": 39.99},
    {"asin": "B09XS7JWHH", "nome": "Sony WH-1000XM5", "idealo": 299.00},
    {"asin": "B0CHX2F5QT", "nome": "Apple AirTag", "idealo": 39.00},
]

def get_price(asin):
    try:
        url = f"https://www.amazon.it/dp/{asin}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        for sel in ["#corePriceDisplay_desktop_feature_div .a-price .a-offscreen", ".a-price .a-offscreen"]:
            el = soup.select_one(sel)
            if el:
                m = re.search(r"(\d+[,\.]\d+)", el.get_text())
                if m:
                    return float(m.group(1).replace(",","."))
        m = re.search(r"€\s*(\d+,\d+)", soup.get_text())
        if m:
            return float(m.group(1).replace(",","."))
    except Exception as e:
        print(f"Errore {asin}: {e}")
    return None

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": False})

random.shuffle(PRODOTTI)
for p in PRODOTTI:
    time.sleep(2)
    prezzo = get_price(p["asin"])
    print(f"Check {p['nome']}: Amazon {prezzo} vs Idealo {p['idealo']}")
    if prezzo and prezzo < p["idealo"] * 0.75:
        sconto = int(100 - (prezzo*100/p["idealo"]))
        link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"
        msg = f"""💎 *FUORI PREZZO LIVE* -{sconto}%

🎧 *{p['nome']}*
💰 Amazon: *{prezzo:.2f}€* invece di {p['idealo']:.2f}€

👉 [COMPRA SU AMAZON]({link})"""
        send(msg)
        break
else:
    print("Nessun fuori prezzo reale oggi - non posto")
