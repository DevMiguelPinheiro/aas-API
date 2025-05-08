import uvicorn
from src.api.logger import logger

if __name__ == "__main__":
    port = 8000
    uvicorn.run("src.api.main:app", port=port, log_level="warning", host="0.0.0.0")
