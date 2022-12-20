# https://www.eclipse.org/paho/index.php?page=clients/python/index.php
import paho.mqtt.client as mqtt

from .FuncionesArchivos import ObtenerValor
from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)


def EnviarMensajeMQTT(Topic, Mensaje, Usuario=None, Contrasenna=None, Servidor=None, Puerto=None):
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
    try:
        MiMQTTSimple = mqtt.Client()
        if Usuario is not None and Contrasenna is not None:
            MiMQTTSimple.username_pw_set(Usuario, Contrasenna)
        MiMQTTSimple.connect(Servidor, Puerto)
        MiMQTTSimple.publish(Topic, Mensaje)
        MiMQTTSimple.disconnect()
        logger.info(f"MQTT[{Topic}] {Mensaje}")
    except Exception as error:
        logger.error(f"MQTT[Error] No se puedo enviar [{Topic}]{Mensaje} - {error}")
