# https://python-telegram-bot.org/

"""Librerías para mandar mensajes de telegram"""
import asyncio
import telegram

from .FuncionesArchivos import ObtenerValor
from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)


def EnviarMensajeTelegram(mensaje, tokenBot=None, idChat=None):
    """Envía un mensaje por telegram."""
    if tokenBot is None:
        tokenBot = ObtenerValor("data/TelegramBot.json", "Token_Telegram")
    if idChat is None:
        idChat = ObtenerValor("data/TelegramBot.json", "ID_Chat")

    if tokenBot is None or idChat is None or tokenBot == "" or idChat == "":
        logger.error("No hay token de telegram")
        return

    try:
        bot = telegram.Bot(token=tokenBot)
        mensaje = mensaje.replace("_", "\\_")
        asyncio.run(bot.send_message(chat_id=idChat, text=mensaje, parse_mode="Markdown"))
    except Exception as err:
        print(f"TelegramBot[Error] {err}")