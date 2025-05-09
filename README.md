# Asset Administration Shell API

Um backend usado para servir e historizar metamodelos de AAS seguindo a estrutura utilizada por arquivos .aasx encontrada em [Metamodel v3](https://industrialdigitaltwin.org/wp-content/uploads/2024/06/IDTA-01001-3-0-1_SpecificationAssetAdministrationShell_Part1_Metamodel.pdf).

## Diagrama de Classes

```mermaid
classDiagram
    class BaseElement {
        +str id_short
        +Optional[DataElementCategory] category
        +Optional[str] description
    }

    class Property {
        +Union[str, float, int] value
        +ValueType value_type
        +validate_value_type()
    }

    class SubmodelElementCollection {
        +List[Union[Property, SubmodelElementCollection]] value
    }

    class Submodel {
        +str id
        +List[Union[Property, SubmodelElementCollection]] submodel_elements
    }

    class AssetAdministrationShell {
        +str id
        +str id_short
        +List[Submodel] data_elements
    }

    class MQTTService {
        -MQTTClient _client
        -bool _connected
        +TOPIC_TEMPERATURE
        +MQTT_BROKER
        +MQTT_PORT
        +_on_connect()
        +_on_disconnect()
        +_on_message()
        +publish_feeding_time_update()
        +register_temperature_callback()
    }

    BaseElement <|-- Property
    BaseElement <|-- SubmodelElementCollection
    BaseElement <|-- Submodel
    SubmodelElementCollection o-- Property
    SubmodelElementCollection o-- SubmodelElementCollection
    Submodel o-- Property
    Submodel o-- SubmodelElementCollection
    AssetAdministrationShell o-- Submodel
    MQTTService ..> Property : updates
```

## Funcionalidades

### AAS (Asset Administration Shell)
- Gerenciamento completo do AAS
- Suporte a submodelos e coleções
- Propriedades variáveis e constantes
- Validação de tipos de dados
- Persistência em MongoDB

### Monitoramento de Temperatura
- Coleta de dados de temperatura via MQTT
- Histórico de temperaturas
- Armazenamento em tempo real
- API para consulta de histórico

### Sistema de Alimentação
- Gerenciamento de horários de alimentação
- Atualização em tempo real via MQTT
- Configuração flexível de horários
- Integração com dispositivos IoT

## Tecnologias Utilizadas

- FastAPI
- MongoDB
- MQTT (gmqtt)
- Pydantic
- Python 3.12+

## Configuração

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=aas_db
```

5. Inicie o servidor:
```bash
uvicorn src.api.main:app --reload
```

## Documentação da API

A documentação interativa está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do Projeto

```
aas-API/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   ├── models/
│   └── utils/
├── requirements.txt
└── README.md
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

# AAS API

API para gerenciamento de Asset Administration Shell (AAS) com suporte a MQTT para atualizações em tempo real.

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/aas-API.git

# Entre no diretório
cd aas-API

# Instale as dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Configure as variáveis de ambiente no arquivo `.env`:
```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=aas/updates
```

2. Inicie o servidor:
```bash
uvicorn src.api.main:app --reload
```

## 📚 Documentação da API

### AAS Endpoints

#### 1. Obter AAS Completo
```http
GET /aas
```

**Resposta:**
```json
{
    "id": "AAS_1",
    "id_short": "AAS_1",
    "semantic_id": "https://example.com/aas",
    "kind": "Instance",
    "data_elements": [
        {
            "id": "Temperatura_1",
            "id_short": "Temperatura",
            "semantic_id": "https://example.com/temperatura",
            "kind": "Instance",
            "submodel_elements": [
                {
                    "id_short": "CurrentTemperature",
                    "value": "25.5",
                    "value_type": "float"
                },
                {
                    "id_short": "TemperatureHistory",
                    "value": [
                        {
                            "id_short": "Timestamp",
                            "value": "2024-02-20T10:00:00",
                            "value_type": "string"
                        },
                        {
                            "id_short": "Value",
                            "value": "25.5",
                            "value_type": "float"
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### 2. Criar/Atualizar AAS
```http
POST /aas
```

**Requisição:**
```json
{
    "id": "AAS_1",
    "id_short": "AAS_1",
    "semantic_id": "https://example.com/aas",
    "kind": "Instance",
    "data_elements": [
        {
            "id": "Temperatura_1",
            "id_short": "Temperatura",
            "semantic_id": "https://example.com/temperatura",
            "kind": "Instance",
            "submodel_elements": [
                {
                    "id_short": "CurrentTemperature",
                    "value": "25.5",
                    "value_type": "float"
                }
            ]
        }
    ]
}
```

### Propriedades Endpoints

#### 1. Obter Propriedades Variáveis
```http
GET /aas/properties/variable
```

**Resposta:**
```json
[
    {
        "id_short": "CurrentTemperature",
        "value": "25.5",
        "value_type": "float"
    }
]
```

#### 2. Obter Propriedades Constantes
```http
GET /aas/properties/constant
```

**Resposta:**
```json
[
    {
        "id_short": "MaxTemperature",
        "value": "100.0",
        "value_type": "float"
    }
]
```

#### 3. Atualizar Propriedade
```http
PUT /aas/properties/{property_id_short}
```

**Requisição:**
```json
{
    "value": "26.5"
}
```

**Resposta:**
```json
{
    "id_short": "CurrentTemperature",
    "value": "26.5",
    "value_type": "float"
}
```

### Submodelos Endpoints

#### 1. Obter Submodelo por ID
```http
GET /aas/submodels/{submodel_id_short}
```

**Resposta:**
```json
{
    "id": "Temperatura_1",
    "id_short": "Temperatura",
    "semantic_id": "https://example.com/temperatura",
    "kind": "Instance",
    "submodel_elements": [
        {
            "id_short": "CurrentTemperature",
            "value": "25.5",
            "value_type": "float"
        },
        {
            "id_short": "TemperatureHistory",
            "value": [
                {
                    "id_short": "Timestamp",
                    "value": "2024-02-20T10:00:00",
                    "value_type": "string"
                },
                {
                    "id_short": "Value",
                    "value": "25.5",
                    "value_type": "float"
                }
            ]
        }
    ]
}
```

### Temperatura Endpoints

#### 1. Obter Histórico de Temperaturas
```http
GET /temperatures
```

**Resposta:**
```json
[
    {
        "timestamp": "2024-02-20T10:00:00",
        "value": 25.5
    },
    {
        "timestamp": "2024-02-20T10:01:00",
        "value": 25.7
    }
]
```

### Debug Endpoints

#### 1. Visualizar Estrutura do AAS
```http
GET /aas/debug/structure
```

**Resposta:**
```json
{
    "message": "Estrutura do AAS impressa no console"
}
```

#### 2. Visualizar Estrutura Detalhada do AAS
```http
GET /aas/debug/detailed
```

**Resposta:**
```json
{
    "message": "Estrutura detalhada do AAS impressa no console"
}
```

## 🔄 MQTT

A API utiliza MQTT para publicar atualizações em tempo real. As mensagens são publicadas no tópico configurado (padrão: `aas/updates`) no seguinte formato:

```json
{
    "property_id_short": "CurrentTemperature",
    "value": "25.5",
    "timestamp": "2024-02-20T10:00:00"
}
```

## 📝 Notas

- Todas as rotas retornam respostas em formato JSON
- Valores de propriedades podem ser strings, números ou booleanos
- Timestamps são formatados em ISO 8601
- A API inclui validação de tipos e valores
- Todas as rotas são documentadas no Swagger UI (`/docs`)
