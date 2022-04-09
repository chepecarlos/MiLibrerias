# https://www.eclipse.org/paho/index.php?page=clients/python/index.php
import paho.mqtt.client as mqtt

from .FuncionesArchivos import ObtenerValor
from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)


def EnviarMensajeMQTT(Topic, Mensaje, Usuario=None, Contrasenna=None, Servidor=None, Puerto=None, Depuracion=True):
    """Envia un Mensaje Simple por MQTT."""
    # TODO: Verificar que Existe Archivo MQTT.json
    ArchivoData = "data/mqtt.json"
    if Usuario is None:
        Usuario = ObtenerValor(ArchivoData, "usuario")
    if Contrasenna is None:
        Contrasenna = ObtenerValor(ArchivoData, "contrasenna")
    if Servidor is None:
        Servidor = ObtenerValor(ArchivoData, "servidor")
    if Puerto is None:
        Puerto = ObtenerValor(ArchivoData, "puerto")
    MiMQTTSimple = mqtt.Client()
    MiMQTTSimple.username_pw_set(Usuario, Contrasenna)
    MiMQTTSimple.connect(Servidor, Puerto)
    MiMQTTSimple.publish(Topic, Mensaje)
    MiMQTTSimple.disconnect()
    if Depuracion:
        logger.info(f"MQTT[{Topic}] {Mensaje}")
