from fastapi import APIRouter, HTTPException
from src.api.services import aas_service
from src.models.models import AssetAdministrationShell

router = APIRouter()

@router.get("/aas", response_model=AssetAdministrationShell)
async def get_aas():
    return aas_service.get_aas()

@router.post("/aas", response_model=AssetAdministrationShell)
async def create_aas(aas: AssetAdministrationShell):
    return aas_service.create_or_update_aas(aas)

@router.get("/aas/properties/variable")
async def get_variable_properties():
    return aas_service.get_variable_properties()

@router.get("/aas/properties/constant")
async def get_constant_properties():
    return aas_service.get_constant_properties()

@router.put("/aas/properties/{property_id_short}")
async def update_property(property_id_short: str, value: str):
    return aas_service.update_property(property_id_short, value)
