FROM docker/compose:latest

WORKDIR /app

COPY . .

CMD ["docker-compose", "up"]