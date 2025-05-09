from fastapi import HTTPException
from src.api.database import colecao
from src.models.models import AssetAdministrationShell, Property, SubmodelElementCollection
from src.utils.converter import create_aas, collect_variable_properties
from src.api.logger import logger
from typing import Union, List, Optional
from src.api.services.mqtt_service import MQTTService

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

def initialize_aas() -> AssetAdministrationShell:
    """
    Initializes the AAS by creating it from the AASX file and saving it to the database.
    This is typically called during application startup.
    If an AAS already exists in the database, it will not create a new one.
    """
    try:
        # Check if AAS already exists in database
        existing_aas = colecao.find_one()
        if existing_aas:
            logger.info("✅ AAS já existe no banco de dados. Usando AAS existente.")
            return AssetAdministrationShell(**existing_aas)

        # Create AAS from AASX file if it doesn't exist
        logger.info("📝 Criando novo AAS a partir do arquivo AASX...")
        aas_instance = create_aas()
        
        # Save to database
        return create_or_update_aas(aas_instance)
    except Exception as e:
        logger.error(f"Failed to initialize AAS: {str(e)}")
        raise

def find_property_by_id_short(elements: List[Union[Property, SubmodelElementCollection]], 
                            target_id_short: str) -> Optional[Property]:
    """
    Recursively searches for a property by its id_short in the AAS structure
    """
    for element in elements:
        if isinstance(element, Property) and element.id_short == target_id_short:
            return element
        elif isinstance(element, SubmodelElementCollection):
            # If the element is a collection, search in its value
            if isinstance(element.value, list):
                found = find_property_by_id_short(element.value, target_id_short)
                if found:
                    return found
    return None

async def update_property(property_id_short: str, value: str) -> dict:
    """
    Atualiza uma propriedade específica do AAS.
    
    Args:
        property_id_short: ID da propriedade a ser atualizada
        value: Novo valor da propriedade
    """
    try:
        # Verificar se a propriedade existe
        property_path = find_property_path(property_id_short)
        if not property_path:
            raise ValueError(f"Propriedade '{property_id_short}' não encontrada")
        
        # Atualizar o valor
        update_value_in_path(property_path, value)
        
        # Se for uma propriedade de horário de alimentação, publicar no MQTT
        if "FeedingTime" in property_id_short:
            mqtt_service = MQTTService()
            await mqtt_service.publish_feeding_time_update(property_id_short, value)
        
        # Salvar no banco de dados
        colecao.update_one(
            {"id": "AAS_1"},
            {"$set": {f"assetInformation.{property_path}": value}}
        )
        
        return {"message": f"Propriedade '{property_id_short}' atualizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

def find_property_path(property_id_short: str) -> Optional[str]:
    """
    Encontra o caminho completo para uma propriedade no AAS.
    
    Args:
        property_id_short: ID da propriedade a ser encontrada
        
    Returns:
        Caminho completo da propriedade ou None se não encontrada
    """
    aas = get_aas()
    
    # Para propriedades de horário de alimentação
    if property_id_short in ["FirstFeedingTime", "SecondFeedingTime", "LastFeedingTime"]:
        return f"FishFeeding.FeedingSchedule.{property_id_short}"
    
    # Para outras propriedades
    for submodel in aas.data_elements:
        # Procurar diretamente no submodel
        for element in submodel.submodel_elements:
            if isinstance(element, Property) and element.id_short == property_id_short:
                return f"{submodel.id_short}.{property_id_short}"
            elif isinstance(element, SubmodelElementCollection):
                # Procurar dentro da coleção
                for sub_element in element.value:
                    if isinstance(sub_element, Property) and sub_element.id_short == property_id_short:
                        return f"{submodel.id_short}.{element.id_short}.{property_id_short}"
    
    return None

def find_property_path_in_elements(elements: List[Union[Property, SubmodelElementCollection]], 
                                 target_id_short: str,
                                 current_path: str = "") -> Optional[str]:
    """
    Busca recursivamente o caminho de uma propriedade nos elementos do AAS.
    """
    for element in elements:
        if isinstance(element, Property) and element.id_short == target_id_short:
            return f"{current_path}.{element.id_short}" if current_path else element.id_short
        elif isinstance(element, SubmodelElementCollection):
            if isinstance(element.value, list):
                path = find_property_path_in_elements(
                    element.value, 
                    target_id_short,
                    f"{current_path}.{element.id_short}" if current_path else element.id_short
                )
                if path:
                    return path
    return None

def update_value_in_path(property_path: str, value: str):
    """
    Atualiza o valor de uma propriedade no AAS usando seu caminho completo.
    
    Args:
        property_path: Caminho completo da propriedade
        value: Novo valor
    """
    aas = get_aas()
    path_parts = property_path.split('.')
    
    # Navegar até o submodel
    current = None
    for submodel in aas.data_elements:
        if submodel.id_short == path_parts[0]:
            current = submodel
            break
    
    if not current:
        raise ValueError(f"Submodel '{path_parts[0]}' não encontrado")
    
    # Se tiver apenas duas partes (submodel.propriedade)
    if len(path_parts) == 2:
        found = False
        for element in current.submodel_elements:
            if isinstance(element, Property) and element.id_short == path_parts[1]:
                element.value = value
                found = True
                break
        if not found:
            raise ValueError(f"Propriedade '{path_parts[1]}' não encontrada em {path_parts[0]}")
    # Se tiver três partes (submodel.coleção.propriedade)
    else:
        # Encontrar a coleção
        collection = None
        for element in current.submodel_elements:
            if isinstance(element, SubmodelElementCollection) and element.id_short == path_parts[1]:
                collection = element
                break
        
        if not collection:
            raise ValueError(f"Coleção '{path_parts[1]}' não encontrada em {path_parts[0]}")
        
        # Atualizar a propriedade na coleção
        found = False
        for element in collection.value:
            if isinstance(element, Property) and element.id_short == path_parts[2]:
                element.value = value
                found = True
                break
        
        if not found:
            raise ValueError(f"Propriedade '{path_parts[2]}' não encontrada em {path_parts[1]}")
    
    # Salvar as alterações
    create_or_update_aas(aas)

def print_aas_structure():
    """Função auxiliar para debug - imprime a estrutura do AAS"""
    aas = get_aas()
    print("\nEstrutura do AAS:")
    for submodel in aas.data_elements:
        print(f"\nSubmodel: {submodel.id_short}")
        for element in submodel.submodel_elements:
            if isinstance(element, Property):
                print(f"  Property: {element.id_short} = {element.value}")
            elif isinstance(element, SubmodelElementCollection):
                print(f"  Collection: {element.id_short}")
                for sub_element in element.value:
                    if isinstance(sub_element, Property):
                        print(f"    Property: {sub_element.id_short} = {sub_element.value}")

def debug_aas_structure():
    """Função para debug - imprime a estrutura exata do AAS"""
    aas = get_aas()
    print("\nEstrutura detalhada do AAS:")
    for submodel in aas.data_elements:
        print(f"\nSubmodel: {submodel.id_short} (id: {submodel.id})")
        print("  Elementos:")
        for element in submodel.submodel_elements:
            if isinstance(element, Property):
                print(f"    Property: {element.id_short} = {element.value} (tipo: {element.value_type})")
            elif isinstance(element, SubmodelElementCollection):
                print(f"    Collection: {element.id_short}")
                print("      Elementos da coleção:")
                for sub_element in element.value:
                    if isinstance(sub_element, Property):
                        print(f"        Property: {sub_element.id_short} = {sub_element.value} (tipo: {sub_element.value_type})")

def get_submodel_by_id_short(submodel_id_short: str):
    """
    Busca um submodelo específico pelo seu idShort.
    
    Args:
        submodel_id_short: ID do submodelo a ser buscado
        
    Returns:
        O submodelo encontrado ou None se não encontrado
    """
    aas = get_aas()
    for submodel in aas.data_elements:
        if submodel.id_short == submodel_id_short:
            return submodel
    return None
