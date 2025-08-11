import os
import requests
from flask import Flask, request

TOKEN = "7989897637:AAHokAnLsUGvZ1KBuTUIOTD5pou9HgPZnvM"
CHAT_ID = "5107123707"
WEBHOOK_URL = f"https://{os.environ.get('RAILWAY_STATIC_URL')}/webhook"

app = Flask(__name__)

# Configuración inicial del webhook
def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    r = requests.post(url, data=data)
    print("Webhook set:", r.json())

# Enviar mensaje a tu chat
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# Endpoint del webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.lower() == "/start":
            send_message("Bot de ofertas iniciado ✅")
        else:
            send_message(f"Recibí tu mensaje: {text}")

    return "OK", 200

@app.route("/")
def home():
    return "Bot de ofertas activo ✅"

if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
