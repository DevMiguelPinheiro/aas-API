from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.api.logger import logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        duration = (time.time() - start_time) * 1000

        logger.info(f"➡️  {request.method} {request.url.path} "
                    f"(status: {response.status_code}, {duration:.2f}ms)")

        return response
