import logging

logger = logging.getLogger("aas_api")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

# Evita múltiplos handlers ao recarregar
if not logger.hasHandlers():
    logger.addHandler(console_handler)
