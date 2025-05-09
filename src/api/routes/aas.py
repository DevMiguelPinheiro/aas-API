from fastapi import APIRouter, HTTPException, Body
from src.api.services import aas_service
from src.models.models import AssetAdministrationShell
from typing import Union
from pydantic import BaseModel

class PropertyUpdate(BaseModel):
    value: Union[str, int, float]

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
async def update_property(property_id_short: str, update: PropertyUpdate):
    """
    Atualiza uma propriedade específica do AAS.
    
    Args:
        property_id_short: ID da propriedade a ser atualizada
        update: Objeto contendo o novo valor da propriedade
    """
    return await aas_service.update_property(property_id_short, str(update.value))

@router.get("/aas/submodels/{submodel_id_short}")
async def get_submodel_by_id_short(submodel_id_short: str):
    """
    Busca um submodelo específico pelo seu idShort.
    
    Args:
        submodel_id_short: ID do submodelo a ser buscado
    """
    submodel = aas_service.get_submodel_by_id_short(submodel_id_short)
    if not submodel:
        raise HTTPException(status_code=404, detail=f"Submodelo com idShort '{submodel_id_short}' não encontrado")
    return submodel

@router.get("/aas/debug/structure")
async def debug_structure():
    """Rota temporária para debug - mostra a estrutura do AAS"""
    from src.api.services.aas_service import print_aas_structure
    print_aas_structure()
    return {"message": "Estrutura do AAS impressa no console"}

@router.get("/aas/debug/detailed")
async def debug_detailed():
    """Rota temporária para debug - mostra a estrutura detalhada do AAS"""
    from src.api.services.aas_service import debug_aas_structure
    debug_aas_structure()
    return {"message": "Estrutura detalhada do AAS impressa no console"}
