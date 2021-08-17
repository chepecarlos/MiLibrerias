import paho.mqtt.client as mqtt

from .FuncionesLogging import ConfigurarLogging
from .FuncionesArchivos import ObtenerValor

logger = ConfigurarLogging(__name__)


def EnviarMensajeMQTT(Topic, Mensaje):
    """Envia un Mensaje Simple por MQTT."""
    Usuario = ObtenerValor("data/MQTT.json", "Usuario")
    Contrasenna = ObtenerValor("data/MQTT.json", "Contrasenna")
    Servidor = ObtenerValor("data/MQTT.json", "Servidor")
    Puesto = ObtenerValor("data/MQTT.json", "Puerto")
    MiMQTTSimple = mqtt.Client()
    MiMQTTSimple.username_pw_set(Usuario, Contrasenna)
    MiMQTTSimple.connect(Servidor, Puesto)
    MiMQTTSimple.publish(Topic, Mensaje)
    logger.info(f"Enviando por MQTT {Topic} - {Mensaje}")
