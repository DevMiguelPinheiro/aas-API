#!/bin/bash

echo "[INFO] Iniciando MongoDB..."
service mongodb start

echo "[INFO] Iniciando InfluxDB..."
service influxdb start

echo "[INFO] Iniciando Mosquitto..."
service mosquitto start

echo "[INFO] Aguardando 10 segundos para os serviços subirem..."
sleep 10

echo "[INFO] Iniciando Eclipse BaSyx..."
java -jar /app/basyx/aas-environment.jar
