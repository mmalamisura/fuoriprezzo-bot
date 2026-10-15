import requests, os
TOKEN = os.getenv("TELEGRAM_TOKEN")
TAG = "fuoriprezzoli-21"
CHANNEL = "@fuoriprezzolive"

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHANNEL, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

# Link che NON dà mai 404 perché usa la ricerca Amazon
link = f"https://www.amazon.it/s?k=Echo+Dot+5&tag={TAG}"

msg = f"""💎 *FUORI PREZZO LIVE* -38%

🎧 Echo Dot 5ª generazione
💰 Amazon: *42€* invece di 69€

👉 [COMPRA SU AMAZON]({link})

#offerta #amazon"""

send(msg)
