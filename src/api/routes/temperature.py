from fastapi import APIRouter, HTTPException
from src.api.services import temperature_service

router = APIRouter()

@router.get("/temperatures")
async def get_temperatures():
    try:
        return temperature_service.get_temperatures()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar temperaturas: {e}")
