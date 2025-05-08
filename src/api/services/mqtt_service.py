### src/api/mqtt_client.py
import asyncio
import json
from datetime import datetime
from typing import Optional, Callable, Any
from gmqtt import Client as MQTTClient
from gmqtt.mqtt.constants import MQTTv311
from src.api.database import colecao_temperatura
from src.api.logger import logger

class MQTTService:
    _instance: Optional['MQTTService'] = None
    _client: Optional[MQTTClient] = None
    _connected: bool = False
    _on_temperature_message: Optional[Callable[[float], Any]] = None

    TOPIC_TEMPERATURE = 'iTamba/temperature'
    MQTT_BROKER = 'broker.hivemq.com'
    MQTT_PORT = 1883

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQTTService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            client_id = f"aas-service-{id(self)}"
            self._client = MQTTClient(client_id)
            self._client.on_connect = self._on_connect
            self._client.on_disconnect = self._on_disconnect
            self._client.on_message = self._on_message
            asyncio.create_task(self._connect())
            logger.info("Iniciando conexão com o broker MQTT")
        except Exception as e:
            logger.warning(f"Erro ao inicializar MQTT: {str(e)}")
            self._client = None

    async def _connect(self):
        try:
            await self._client.connect(self.MQTT_BROKER, self.MQTT_PORT, version=MQTTv311)
        except Exception as e:
            logger.warning(f"Erro ao conectar no broker: {str(e)}")
            self._connected = False

    def _on_connect(self, client, flags, rc, properties):
        self._connected = True
        logger.info("✅ Conectado ao broker MQTT")
        client.subscribe(self.TOPIC_TEMPERATURE)

    def _on_disconnect(self, client, packet, exc=None):
        self._connected = False
        logger.warning(f"🔌 Desconectado do broker MQTT: {str(exc)}")

    def _on_message(self, client, topic, payload, qos, properties):
        try:
            decoded = payload.decode()
            logger.info(f"📥 Mensagem recebida no tópico {topic}: {decoded}")

            try:
                data = json.loads(decoded)
                temperature = data["temperature"]
            except (json.JSONDecodeError, TypeError, KeyError):
                temperature = float(decoded)

            colecao_temperatura.insert_one({
                "temperature": temperature,
                "timestamp": datetime.now()
            })
            logger.info(f"🌡️ Temperatura salva: {temperature}°C")

            if topic == self.TOPIC_TEMPERATURE and self._on_temperature_message:
                self._on_temperature_message(temperature)

        except Exception as e:
            logger.error(f"Erro ao processar mensagem MQTT: {str(e)}")

    async def publish_feeding_time_update(self, property_id: str, value: str):
        """
        Publica uma atualização de horário de alimentação no tópico MQTT
        
        Args:
            property_id: ID da propriedade (ex: FirstFeedingTime)
            value: Novo valor do horário
        """
        if not self._client or not self._connected:
            logger.warning("MQTT não conectado – publicação ignorada")
            return

        topic = f"FishTankAAS/FishFeeding/{property_id}"
        payload = json.dumps({
            "property_id": property_id,
            "value": value,
            "timestamp": datetime.now().isoformat()
        })

        try:
            # Publicar a mensagem diretamente
            self._client.publish(topic, payload, qos=1, retain=False)
            logger.info(f"📤 Publicado no tópico {topic}: {payload}")
        except Exception as e:
            logger.error(f"Erro ao publicar: {str(e)}")

    def register_temperature_callback(self, callback: Callable[[float], Any]):
        self._on_temperature_message = callback

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client and self._connected:
            await self._client.disconnect()
