import paho.mqtt.client as mqtt

from .FuncionesLogging import ConfigurarLogging
from .FuncionesArchivos import ObtenerDato

logger = ConfigurarLogging(__name__)


def EnviarMensajeMQTT(Topic, Mensaje):
    """Envia un Mensaje Simple por MQTT."""
    Usuario = ObtenerDato("/Data/MQTT.json", "Usuario")
    Contrasenna = ObtenerDato("/Data/MQTT.json", "Contrasenna")
    Servidor = ObtenerDato("/Data/MQTT.json", "Servidor")
    Puesto = ObtenerDato("/Data/MQTT.json", "Puerto")
    MiMQTTSimple = mqtt.Client()
    MiMQTTSimple.username_pw_set(Usuario, Contrasenna)
    MiMQTTSimple.connect(Servidor, Puesto)
    MiMQTTSimple.publish(Topic, Mensaje)
    logger.info(f"Enviando por MQTT {Topic} - {Mensaje}")
