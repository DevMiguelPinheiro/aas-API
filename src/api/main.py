from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import aas, temperature
from src.api.services.mqtt_service import MQTTService
from src.api.logger import logger
from src.api.middleware.logger_middleware import LoggingMiddleware
from src.api.services import aas_service
import asyncio

app = FastAPI(title="AAS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(aas.router)
app.include_router(temperature.router)

@app.on_event("startup")
async def startup():
    # Initialize AAS
    try:
        aas_instance = aas_service.initialize_aas()
        logger.info(f"✅ AAS inicializado com sucesso! ID: {aas_instance.id}")
        logger.info("🚀 AAS API inicializada com sucesso!")
        logger.info("🔗 Endpoints disponíveis:")
        logger.info("")
        logger.info("📌 AAS Endpoints:")
        logger.info("   → GET    /aas")
        logger.info("     • Retorna o AAS completo")
        logger.info("")
        logger.info("📌 Propriedades Endpoints:")
        logger.info("   → GET    /aas/properties/variable")
        logger.info("     • Retorna todas as propriedades variáveis")
        logger.info("")
        logger.info("   → GET    /aas/properties/constant")
        logger.info("     • Retorna todas as propriedades constantes")
        logger.info("")
        logger.info("   → PUT    /aas/properties/{property_id_short}")
        logger.info("     • Atualiza uma propriedade específica")
        logger.info("")
        logger.info("📌 Temperatura Endpoints:")
        logger.info("   → GET    /temperatures")
        logger.info("     • Retorna histórico de temperaturas")
        logger.info("")

        # Initialize MQTT
        mqtt_service = MQTTService()
        logger.info("✅ Serviço MQTT inicializado")

    except Exception as e:
        logger.error(f"❌ Falha ao inicializar AAS: {str(e)}")
