from fastapi import HTTPException
from src.api.database import colecao
from src.models.models import AssetAdministrationShell
from src.utils.converter import create_aas, collect_variable_properties

def get_aas():
    aas = colecao.find_one()
    if not aas:
        raise HTTPException(status_code=404, detail="AAS not found")
    return AssetAdministrationShell(**aas)

def create_or_update_aas(aas: AssetAdministrationShell):
    aas_dict = aas.model_dump()
    existing = colecao.find_one({"id": aas.id})
    if existing:
        colecao.replace_one({"id": aas.id}, aas_dict)
    else:
        colecao.insert_one(aas_dict)
    return aas

def get_variable_properties():
    aas = get_aas()
    properties = []
    for submodel in aas.data_elements:
        properties.extend(collect_variable_properties(submodel.submodel_elements))
    return properties

def get_constant_properties():
    aas = get_aas()
    # lógica similar para CONSTANT
    return []

def update_property(property_id_short: str, value: str):
    aas = get_aas()
    # lógica de update
    return {"message": "Updated"}
