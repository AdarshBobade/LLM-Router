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
        groq_response = tg.create_task(llm1.fetch(prompt))
        gemini_response = tg.create_task(llm2.fetch(prompt))
        hf_response = tg.create_task(llm3.fetch(prompt))
    
    print('Groq ->', groq_response.result())
    print('Gemini ->' , gemini_response.result())
    print('HuggingFace ->' , hf_response.result())

asyncio.run(main())

    


    
    
# asyncio.run(main())

   




