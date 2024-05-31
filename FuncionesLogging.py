"""Libreria de logging."""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from logging import Logger


def FoldeLog() -> str:
    """Devuelte ruta donde esta el folder de configuracion."""
    Programa = os.path.basename(sys.argv[0]).lower()
    Programa = os.path.splitext(Programa)[0]
    Programa = str(Programa).split("_")[0]

    Folder = os.path.join(".config", Programa)
    Folder = os.path.join(Path.home(), Folder)
    Folder = os.path.join(Folder, "logs")

    return Folder


def ConfigurarLogging(Nombre, NivelLog=logging.INFO) -> Logger:
    """Configura el archivo de depuración."""
    #TODO: Nivel de depuracion
    logger = logging.getLogger(Nombre)
    logger.setLevel(NivelLog)

    ArchivoLog = FoldeLog()

    if not os.path.isdir(ArchivoLog):
        os.makedirs(ArchivoLog)

    # Agrega Fecha actua a log
    ArchivoLog = ArchivoLog + "/{:%Y-%m-%d_%H:%M:%S}.log".format(datetime.now())

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(ArchivoLog)
    c_format = logging.Formatter("%(name)s-%(message)s")
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
