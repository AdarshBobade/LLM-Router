import time
import httpx
import asyncio

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
