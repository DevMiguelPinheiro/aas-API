FROM docker/compose:latest

WORKDIR /app

COPY . .

# Expõe todas as portas necessárias
EXPOSE 3000 3081 3082 3083 3084 3085 3086 1885 3017

# Comando para iniciar os serviços
CMD ["docker-compose", "up"]