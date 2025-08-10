import os
import sys
import telebot

# Leer token desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Validar token antes de iniciar el bot
if not TELEGRAM_TOKEN:
    print("❌ ERROR: No se encontró la variable TELEGRAM_TOKEN en Railway.")
    print("💡 Ve a Settings → Variables y agrega TELEGRAM_TOKEN con tu token completo.")
    sys.exit(1)

if ":" not in TELEGRAM_TOKEN:
    print("❌ ERROR: El token de Telegram no es válido. Falta el formato con ':'")
    print("💡 Ejemplo de formato correcto: 123456789:ABCDefghIJKlmNoPQRstUvwxYZ")
    sys.exit(1)

# Crear bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Ejemplo de comando
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! El bot está funcionando correctamente ✅")

# Iniciar bot
if __name__ == "__main__":
    print("🚀 Bot iniciado correctamente.")
    bot.infinity_polling()
