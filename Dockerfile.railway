# Usa uma imagem base do Ubuntu
FROM ubuntu:latest

# Atualiza pacotes e instala dependências
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    nano \
    sudo \
    openjdk-17-jdk \
    mongodb \
    influxdb \
    mosquitto \
    mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Baixa e instala o Eclipse BaSyx
RUN mkdir -p /app/basyx
COPY basyx/ /app/basyx/

# Baixa e instala o Telegraf
COPY telegraf/ /etc/telegraf/
RUN chmod +x /etc/telegraf/telegraf.conf || true

# Copia os arquivos do projeto para o container
COPY . /app/

# Configura permissões
RUN chmod +x /app/start.sh || true

# Expõe as portas necessárias
EXPOSE 1883 8080 8081 8086 9999 3000 27017

# Define o script de inicialização como ponto de entrada
CMD ["/bin/bash", "/app/start.sh"]
