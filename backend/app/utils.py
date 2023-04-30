from contextlib import asynccontextmanager, contextmanager
from functools import wraps
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# def log_entry_exit(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         start_time = time.time()
#         logger.debug(f"----- BEGIN {func.__name__} -----")
#         result = await func(*args, **kwargs)
#         elapsed_time = time.time() - start_time
#         logger.debug(f"Execution time: {elapsed_time:.2f} seconds")
#         logger.debug(f"----- END {func.__name__} -----")
#         return result
#     return wrapper

def log_time_func(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        logger.info(f"FUNC {func.__name__} took {round(end - start, 2)} seconds")
        return result

    return wrapper

@asynccontextmanager
async def log_time_async(statement_name: str):
    start = time.time()
    yield
    end = time.time()
    logger.info(f"LINE: {statement_name} took {round(end - start, 2)} seconds")

@contextmanager
def log_time_sync(statement_name: str):
    start = time.time()
    yield
    end = time.time()
    logger.info(f"LINE: {statement_name} took {round(end - start, 2)} seconds")