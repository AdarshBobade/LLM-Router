import asyncio
import os
import time
import httpx
from dotenv import load_dotenv
load_dotenv()
from abc import ABC,abstractmethod
from providers import Groq , Gemini , HuggingFace

groq_api = os.getenv('GROQ_API_KEY')
gemini_api = os.getenv('GEMINI_API_KEY')
hf_api = os.getenv('HUGGINGFACE_TOKEN')


async def main():
    prompt = input('Ask the LLMs ->')
    llm1 = Groq(groq_api)
    llm2 = Gemini(gemini_api)
    llm3 = HuggingFace(hf_api)
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(llm1.fetch(prompt))
        task2 = tg.create_task(llm2.fetch(prompt))
        task3 = tg.create_task(llm3.fetch(prompt))
    
    groq_response , groq_latency = task1.result()
    gemini_response , gemini_latency = task2.result()
    hf_response , hf_latency = task3.result()

    print('Groq ->', groq_response)
    print('Gemini ->' , gemini_response)
    print('HuggingFace ->' , hf_response)
    print('time_elapsed by Groq :' , groq_latency)
    print('time_elapsed by Gemini :' , gemini_latency)
    print('time_elapsed by HuggingFace :' , hf_latency)


asyncio.run(main())

    


    
    
# asyncio.run(main())

   




