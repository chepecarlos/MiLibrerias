"""Librería de logging."""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from logging import Logger

import colorlog
import inspect


def nombrePrograma() -> str:
    """Obtiene el nombre del paquete o módulo principal."""

    frame = inspect.currentframe()
    module = inspect.getmodule(frame.f_back)
    if module and module.__package__:
        return module.__package__.split(".")[0].lower()
    elif module:
        return module.__name__.split(".")[0].lower()
    return "unknown"


def FoldeLog() -> str:
    """Devuelve ruta donde esta el folder de configuración."""
    Programa = nombrePrograma()

    Folder = os.path.join(".config", Programa)
    Folder = os.path.join(Path.home(), Folder)
    Folder = os.path.join(Folder, "logs")

    return Folder


def ConfigurarLogging(
    Nombre: str,
    NivelLog: int = logging.WARNING
    ) -> Logger:
    """Configura el logger con salida en consola y archivo.

    Args:
        NivelLog (int): Nivel de logging (por defecto, logging.WARNING).

    Returns:
        Logger: Objeto logger configurado

    """

    if "--depuracion" in sys.argv:
        NivelLog = logging.DEBUG
    
    # Atributos de logger https://docs.python.org/3/library/logging.html#logrecord-attributes
    FormatoMensaje: str = "%(asctime)s %(process)d %(processName)s %(log_color)s%(module)s-%(funcName)s[%(levelname)s]%(reset)s: %(message)s"
    
    FormatoMensaje: str = "%(asctime)s %(process)d %(processName)s %(log_color)s%(module)s-%(funcName)s[%(levelname)s]%(reset)s: %(message)s"
    FormatoTiempo: str = "%I:%M:%S %p"
    
    NombrePrograma = nombrePrograma()

    logger = colorlog.getLogger(Nombre)
    logger.setLevel(NivelLog)
    

    loggerColor = colorlog.StreamHandler()
    loggerColor.setFormatter(colorlog.ColoredFormatter(
        FormatoMensaje, datefmt=FormatoTiempo))
    logger.addHandler(loggerColor)

    ArchivoLog =  os.path.join(FoldeLog(), f"{NombrePrograma}.log")

    if not os.path.isdir(os.path.dirname(ArchivoLog)):
        os.makedirs(os.path.dirname(ArchivoLog))

    loggerArchivo = logging.FileHandler(ArchivoLog)
    format_archivo = logging.Formatter(
        "%(asctime)s %(process)d %(processName)s - %(name)s - %(levelname)s - %(message)s")
    loggerArchivo.setFormatter(format_archivo)
    logger.addHandler(loggerArchivo)

    return logger
