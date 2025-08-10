import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import urllib.parse

# === CONFIGURACIÓN ===
TELEGRAM_TOKEN = "7989897637:AAHokAnLsUGvZ1KBuTUIOTD5pou9HgPZnvM"
CHAT_ID = 5107123707
PALABRAS_CLAVE = [
    "analista", "analista qa", "qa manual", "analista funcional",
    "qa funcional", "soporte mesa de ayuda", "especialista en procesos it",
    "help desk", "it support", "software tester", "qa tester", "qa engineer"
]

# === FUENTES DE EMPLEOS ===
PORTALES = {
    "Bumeran": "https://www.bumeran.com.ar/empleos-busqueda-qa.html",
    "Computrabajo": "https://ar.computrabajo.com/trabajo-de-qa",
    "Indeed": "https://ar.indeed.com/jobs?q=qa&l=Argentina&sort=date",
    "Glassdoor": "https://www.glassdoor.com.ar/Empleo/argentina-qa-empleos-SRCH_IL.0,9_IN185_KO10,12.htm?sortBy=DATE",
    "LinkedIn": "https://www.linkedin.com/jobs/search?keywords=qa&location=Argentina&f_TPR=r86400&sortBy=DD"
}

# === BOT TELEGRAM ===
bot = Bot(token=TELEGRAM_TOKEN)
vistos = set()  # Guarda enlaces ya enviados

def buscar_ofertas():
    nuevas = []
    for nombre, url in PORTALES.items():
        try:
            print(f"Buscando en {nombre}...")
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            enlaces = soup.find_all("a", href=True)

            for link in enlaces:
                titulo = link.get_text().strip().lower()
                href = link["href"]

                # Completar URL si es relativa
                if href.startswith("/"):
                    href = urllib.parse.urljoin(url, href)

                # Filtrar por palabras clave
                if any(palabra in titulo for palabra in PALABRAS_CLAVE):
                    if href not in vistos and "http" in href:
                        vistos.add(href)
                        nuevas.append(f"[{titulo}]({href})")

        except Exception as e:
            print(f"Error en {nombre}: {e}")
    return nuevas

def enviar_mensajes(ofertas):
    for oferta in ofertas:
        try:
            bot.send_message(chat_id=CHAT_ID, text=oferta, parse_mode="Markdown")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

if __name__ == "__main__":
    print("Bot iniciado. Buscando ofertas cada 5 minutos...")
    while True:
        ofertas = buscar_ofertas()
        if ofertas:
            enviar_mensajes(ofertas)
        time.sleep(300)  # Espera 5 minutos
