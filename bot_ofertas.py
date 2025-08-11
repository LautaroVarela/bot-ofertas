import os
import time
import telebot
import requests
from bs4 import BeautifulSoup

# Variables desde Railway (o directo para pruebas locales)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "TU_TOKEN_AQUI")
CHAT_ID = int(os.getenv("CHAT_ID", "5107123707"))

# Inicializar bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Palabras clave para filtrar
KEYWORDS = [
    "remoto",
    "junior",
    "it",
    "analista qa",
    "qa manual",
    "quality assurance",
    "testing"
]

# Lista para guardar ofertas enviadas y evitar duplicados
sent_offers = set()

# URL de ejemplo (reemplazar por tu fuente real de ofertas)
URL = "https://www.computrabajo.com.ar/trabajo-de-it-sistemas"

def fetch_offers():
    """Obtiene ofertas desde la web"""
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        offers = []

        for link in soup.find_all("a", href=True):
            title = link.get_text(strip=True).lower()
            href = link["href"]
            if any(keyword in title for keyword in KEYWORDS):
                full_url = href if href.startswith("http") else "https://www.computrabajo.com.ar" + href
                offers.append((title, full_url))

        return offers
    except Exception as e:
        print(f"Error al obtener ofertas: {e}")
        return []

def send_new_offers():
    """Envía ofertas nuevas a Telegram"""
    offers = fetch_offers()
    for title, url in offers:
        if url not in sent_offers:
            sent_offers.add(url)
            bot.send_message(CHAT_ID, f"🆕 {title}\n{url}")

if __name__ == "__main__":
    print("🤖 Bot iniciado, buscando ofertas cada 5 minutos...")
    while True:
        send_new_offers()
        time.sleep(300)  # 5 minutos
