from pymongo import MongoClient

# Para MongoDB local
# client = MongoClient("mongodb://localhost:27017/")

# Para MongoDB remoto (exemplo com usuário/senha)
client = MongoClient("mongodb://mongoAdmin:mongoPassword@yamabiko.proxy.rlwy.net:41889/")

# Nome do banco de dados
db = client["db_fishTank"]

# Nome da coleção
colecao = db["tank_data"]
colecao_temperatura = db["tank_temperature"]

#Inserindo um documento de exemplo
#documento = {"nome": "Miguel", "idade": 25}
#resultado = colecao.insert_one(documento)

#print("ID do documento inserido:", resultado.inserted_id)

#Buscando e imprimindo todos os documentos
#for doc in colecao.find():
#    print(doc)
