import time
import asyncio
from logging import getLogger
from functools import wraps

logger = getLogger("software-scanner")

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{func.__name__} took {elapsed_time:.2f} seconds")
        return result
    return wrapper