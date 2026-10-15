import requests, os, random
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

PRODOTTI = [
    {"asin": "B09B8X9RGM", "nome": "Echo Dot 5ª Gen - Alexa", "desc": "Suono potente, Alexa, sensore temperatura"},
    {"asin": "B09WX9XBKD", "nome": "Echo Pop - Smart speaker compatto", "desc": "Compatto, colori, Alexa completa"},
    {"asin": "B0BTFSYWWB", "nome": "Fire TV Stick 4K Max 2024", "desc": "WiFi 6E, 16GB, 4K HDR, Alexa+"},
    {"asin": "B09XS7JWHH", "nome": "Sony WH-1000XM5", "desc": "Top noise cancelling, 30h batteria"},
    {"asin": "B0932QJ2BZ", "nome": "Apple AirTag", "desc": "Trova tutto con iPhone"},
]

def send_con_foto(prod):
    link = f"https://www.amazon.it/dp/{prod['asin']}?tag={TAG}"
    # Foto ufficiale Amazon presa da ASIN
    foto_url = f"https://m.media-amazon.com/images/P/{prod['asin']}.01.LZZZZZZZ.jpg"
    caption = f"""🔥 *{prod['nome']}*
{prod['desc']}

✅ Verificato su Amazon.it
🛒 [CLICCA QUI PER VEDERE PREZZO REALE]({link})

Link affiliato attivo - prezzi aggiornati al checkout
#offerta #{prod['asin'][:4]}"""

    # 1. Prova a mandare FOTO + caption
    url_foto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    r = requests.post(url_foto, json={
        "chat_id": CHANNEL,
        "photo": foto_url,
        "caption": caption,
        "parse_mode": "Markdown"
    })
    print(f"Foto {prod['asin']}: {r.status_code} - {r.text[:300]}")

    # 2. Se la foto fallisce, manda solo testo
    if r.status_code!= 200:
        url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        r2 = requests.post(url_msg, json={"chat_id": CHANNEL, "text": caption, "parse_mode": "Markdown"})
        print(f"Testo fallback: {r2.status_code}")

p = random.choice(PRODOTTI)
print(f"Provo a postare {p['nome']} {p['asin']}")
send_con_foto(p)
