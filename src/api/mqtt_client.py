import asyncio
import json
from datetime import datetime
from gmqtt import Client as MQTTClient
from src.api.database import colecao_temperatura
from src.api.logger import logger

# Configurações do broker MQTT
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
TOPIC = 'iTamba/temperature'

client = MQTTClient("aas-api-client")

# Callback para conexão
def on_connect(client, flags, rc, properties):
    logger.info("Conectado ao broker MQTT")
    client.subscribe(TOPIC)

# Callback para mensagens recebidas
def on_message(client, topic, payload, qos, properties):
    try:
        decoded = payload.decode()
        logger.info(f"Mensagem recebida: {decoded}")

        try:
            data = json.loads(decoded)
            # Caso venha como JSON: {"temperature": 27.4}
            temperature = data["temperature"]
        except (json.JSONDecodeError, TypeError):
            # Caso venha como string direta: "27.4"
            temperature = float(decoded)

        colecao_temperatura.insert_one({
            "temperature": temperature,
            "timestamp": datetime.now()
        })

    except Exception as e:
        logger.info(f"Erro ao processar mensagem MQTT: {e}")

# Inicializa e conecta o cliente MQTT
async def start_mqtt():
    client.on_connect = on_connect
    client.on_message = on_message

    await client.connect(MQTT_BROKER, MQTT_PORT)

    # Mantém o loop ativo
    while True:
        await asyncio.sleep(1)
