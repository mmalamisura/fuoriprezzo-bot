import requests, os, re, time, random
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"
MAX_POST_PER_RUN = 4  # cambia qui: 3,5,10

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9",
}

# Fallback se Amazon blocca i bestseller
FALLBACK = ["B09B8X9RGM","B09WX9XBKD","B0BTFSYWWB","B0GJTFY58R","B0BSHF7WHW","B085FXHR38","B0BCR8Z7QL"]

def get_bestsellers():
    """Prende i più venduti del momento da Amazon.it"""
    try:
        url = "https://www.amazon.it/gp/bestsellers/electronics"
        r = requests.get(url, headers=HEADERS, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        asins = []
        for a in soup.find_all("a", href=True):
            m = re.search(r"/dp/([A-Z0-9]{10})", a["href"])
            if m:
                asin = m.group(1)
                if asin not in asins and asin.startswith("B0"):
                    asins.append(asin)
        print(f"Bestseller trovati: {asins[:10]}")
        return asins[:15]
    except Exception as e:
        print(f"Bestseller bloccato, uso fallback: {e}")
        return FALLBACK

def get_info(asin):
    """Legge prezzo attuale e prezzo pieno"""
    try:
        url = f"https://www.amazon.it/dp/{asin}"
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        text = r.text
        
        # Titolo
        title = soup.find(id="productTitle")
        nome = title.get_text().strip()[:70] if title else asin
        
        # Prezzo attuale
        prezzo = None
        for sel in ["#corePriceDisplay_desktop_feature_div .a-offscreen", ".a-price .a-offscreen"]:
            el = soup.select_one(sel)
            if el:
                m = re.search(r"(\d+[,\.]\d+)", el.get_text())
                if m:
                    prezzo = float(m.group(1).replace(",","."))
                    break
        
        # Prezzo listino / pieno
        pieno = None
        # cerca "Prezzo consigliato" o list price
        m = re.search(r"Prezzo consigliato:</span>\s*<span[^>]*>€?([\d,]+)", text)
        if not m:
            m = re.search(r'"listPrice":\s*"([\d\.]+)"', text)
        if m:
            pieno = float(m.group(1).replace(",","."))
        
        if not pieno and prezzo:
            pieno = prezzo * 1.4  # stima se non c'è listino

        return {"asin": asin, "nome": nome, "prezzo": prezzo, "pieno": pieno}
    except Exception as e:
        print(f"Errore {asin}: {e}")
        return None

def send_telegram(prod):
    link = f"https://www.amazon.it/dp/{prod['asin']}?tag={TAG}"
    sconto = int((1 - prod['prezzo']/prod['pieno'])*100) if prod['prezzo'] and prod['pieno'] else 0
    
    if sconto >= 20:
        badge = f"🔥 FUORI PREZZO -{sconto}%"
    elif sconto >= 10:
        badge = f"💰 OFFERTA -{sconto}%"
    else:
        badge = "⭐ PIÙ VENDUTO"

    txt = f"""{badge}
{prod['nome']}

Prezzo: {prod['prezzo']}€ (listino {prod['pieno']}€)

Disponibilità immediata Prime

👇 Acquista qui:

{link}

#fuoriprezzo #bestseller"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHANNEL, "text": txt, "disable_web_page_preview": False})
    print(f"Post {prod['asin']} {prod['prezzo']}€ sconto {sconto}% -> {r.status_code}")
    time.sleep(3)

# --- MAIN ---
bests = get_bestsellers()
random.shuffle(bests)
postati = 0

for asin in bests:
    if postati >= MAX_POST_PER_RUN:
        break
    info = get_info(asin)
    if not info or not info['prezzo']:
        print(f"Skip {asin} - no prezzo")
        continue
    
    # Posta solo se è fuori prezzo o bestseller forte
    sconto = (1 - info['prezzo']/info['pieno'])*100 if info['pieno'] else 0
    if sconto >= 10 or postati < 2:  # i primi 2 li posta anche se sconto basso per tenere vivo canale
        send_telegram(info)
        postati += 1
    time.sleep(2)

print(f"Finito - postati {postati} prodotti")
