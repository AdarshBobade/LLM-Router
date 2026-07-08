import time
import httpx
import asyncio
import functools

def retry(times=3 , delay=1):
    def decorator(func):
        async def wrapper(*args,**kwargs):
            for attempt in range(times):
                try :
                    return await func(*args,**kwargs)
                except httpx.HTTPStatusError:
                    print(f"Attempt {attempt+1} failed, retrying...")
                    await asyncio.sleep(delay)
            raise Exception('All retries failed !')
        return wrapper
    return decorator

def latency(func):
    @functools.wraps(func)
    async def wrapper(*args,**kwargs):
        start = time.perf_counter()
        response = await func(*args,**kwargs)
        end = time.perf_counter()
        time_elapsed = (end - start)
        return response , time_elapsed
    return wrapper

