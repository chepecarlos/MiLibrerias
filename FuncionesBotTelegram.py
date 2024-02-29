# https://python-telegram-bot.org/

"""Librerías para mandar mensajes de telegram"""
import asyncio
import telegram

from .FuncionesArchivos import ObtenerValor
from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)


def EnviarMensajeTelegram(mensaje, tokenBot=None, idChat=None):
    """Enviá un mensaje por telegram."""
    if tokenBot is None:
        tokenBot = ObtenerValor("data/TelegramBot.json", "Token_Telegram")
    if idChat is None:
        idChat = ObtenerValor("data/TelegramBot.json", "ID_Chat")

    if tokenBot is None or idChat is None:
        logger.error("No hay token de telegram")
        return

    bot = telegram.Bot(token=tokenBot)
    asyncio.run(bot.send_message(chat_id=idChat, text=mensaje))
