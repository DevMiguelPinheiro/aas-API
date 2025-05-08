from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import aas, temperature
from src.api.mqtt_client import start_mqtt
from src.api.logger import logger
from src.api.middleware.logger_middleware import LoggingMiddleware
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
    logger.info("🚀 AAS API inicializada com sucesso!")
    logger.info("🔗 Endpoints disponíveis:")
    logger.info("   → /aas")
    logger.info("   → /aas/properties/variable")
    logger.info("   → /aas/properties/constant")
    logger.info("   → /temperatures")
    asyncio.create_task(start_mqtt())
