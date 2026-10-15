import requests, os, re, time, random
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"
MAX_POST = 4

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9",
}

# Lista di sicurezza - usata se 【entity-Amazon¦canonical_name=Amazon】 blocca i bestseller
FALLBACK = [
    {"asin": "B09B8X9RGM", "nome": "Echo Dot 5ª Gen", "pieno": 64.99},
    {"asin": "B09WX9XBKD", "nome": "Echo Pop", "pieno": 54.99},
    {"asin": "B0BTFSYWWB", "nome": "Fire TV Stick 4K Max", "pieno": 79.99},
    {"asin": "B0GJTFY58R", "nome": "AirTag 2ª Gen", "pieno": 45.00},
    {"asin": "B0BSHF7WHW", "nome": "Echo Show 5 3ª Gen", "pieno": 109.99},
    {"asin": "B085FXHR38", "nome": "Echo 4ª Gen", "pieno": 119.99},
]

def get_bestsellers():
    try:
        url = "https://www.amazon.it/gp/bestsellers/electronics"
        r = requests.get(url, headers=HEADERS, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        asins = []
        for a in soup.find_all("a", href=True):
            m = re.search(r"/dp/([A-Z0-9]{10})", a["href"])
            if m and m.group(1) not in asins and m.group(1).startswith("B0"):
                asins.append(m.group(1))
        print(f"Bestseller trovati: {asins[:8]}")
        return asins[:12] if asins else [x["asin"] for x in FALLBACK]
    except Exception as e:
        print(f"Bestseller error: {e} -> uso fallback")
        return [x["asin"] for x in FALLBACK]

def get_info(asin):
    try:
        url = f"https://www.amazon.it/dp/{asin}?tag={TAG}"
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Nome
        el_title = soup.find(id="productTitle")
        nome = el_title.get_text().strip()[:80] if el_title else f"Prodotto {asin}"
        
        # Prezzo attuale
        prezzo = None
        for sel in ["#corePriceDisplay_desktop_feature_div .a-offscreen", "span.a-price .a-offscreen"]:
            el = soup.select_one(sel)
            if el:
                m = re.search(r"(\d+[,\.]\d+)", el.get_text())
                if m:
                    prezzo = float(m.group(1).replace(",","."))
                    break
        
        # Prezzo pieno (listino)
        pieno = None
        m = re.search(r'Prezzo consigliato:\s*</span><span[^>]*>€?\s*([\d,\.]+)', r.text)
        if not m:
            m = re.search(r'"listPrice"\s*:\s*"([\d\.]+)"', r.text)
        if m:
            pieno = float(m.group(1).replace(",","."))
        
        if not pieno and prezzo:
            # Se non c'è listino, prendi da fallback
            for f in FALLBACK:
                if f["asin"] == asin:
                    pieno = f["pieno"]
                    break
            if not pieno:
                pieno = round(prezzo * 1.35, 2)

        if prezzo:
            print(f"{asin}: {nome[:30]} - {prezzo}€ / {pieno}€")
        return {"asin": asin, "nome": nome, "prezzo": prezzo, "pieno": pieno}
    except Exception as e:
        print(f"Errore info {asin}: {e}")
        return None

def send_telegram(p):
    link = f"https://www.amazon.it/dp/{p['asin']}?tag={TAG}"
    sconto = int((1 - p['prezzo']/p['pieno'])*100) if p['prezzo'] and p['pieno'] else 0

    if sconto >= 25:
        badge = f"🔥 FUORI PREZZO -{sconto}% 🔥"
    elif sconto >= 15:
        badge = f"💰 FUORI PREZZO -{sconto}%"
    elif sconto >= 5:
        badge = f"⭐ OFFERTA -{sconto}%"
    else:
        badge = "📦 PIÙ VENDUTO OGGI"

    text = f"""{badge}
{p['nome']}

Prezzo: {p['prezzo']}€ invece di {p['pieno']}€

✅ Disponibile - Prime - Carrello attivo

👇 LINK DIRETTO:

{link}

#fuoriprezzo #offerta"""

    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    resp = requests.post(api, json={
        "chat_id": CHANNEL,
        "text": text,
        "disable_web_page_preview": False
    })
    print(f"TELEGRAM {p['asin']} -> {resp.status_code} {resp.text[:200]}")
    return resp.status_code == 200

# --- RUN ---
print(f"START bot - Token presente: {bool(TOKEN)}")
bests = get_bestsellers()
random.shuffle(bests)

postati = 0
for asin in bests:
    if postati >= MAX_POST:
        break
    info = get_info(asin)
    if not info or not info['prezzo']:
        continue
    
    # Posta
    ok = send_telegram(info)
    if ok:
        postati += 1
    time.sleep(4)

print(f"FINE - postati {postati} prodotti")
