# from MisFunciones import *
import MisFunciones

logger = MisFunciones.ConfigurarLogging(__name__)

print(f"Hola mundo {MisFunciones.ObtenerFolderConfig()}")
logger.info("Prueba")
