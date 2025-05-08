from datetime import datetime
from src.api.database import colecao_temperatura

def get_temperatures():
    registros = colecao_temperatura.find().sort("timestamp", -1).limit(100)
    data = []
    for doc in registros:
        data.append({
            "temperature": doc.get("temperature"),
            "timestamp": doc.get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
        })
    data.reverse()
    return data