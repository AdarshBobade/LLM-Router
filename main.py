import asyncio
import os
import time
import httpx
from dotenv import load_dotenv
load_dotenv()
from abc import ABC,abstractmethod

groq_api = os.getenv('GROQ_API_KEY')
gemini_api = os.getenv('GEMINI_API_KEY')
hf_api = os.getenv('HUGGINGFACE_TOKEN')

class BaseProvider(ABC):
    def __init__(self,api_key):
        self.api_key = api_key
        
    @abstractmethod
    async def fetch(self,prompt):
        pass

class Groq(BaseProvider):
    def __init__(self,api_key):
        super().__init__(api_key)
        self.url = 'https://api.groq.com/openai/v1/chat/completions'
    async def fetch(self,prompt):
        async with httpx.AsyncClient(timeout=10) as client:
            
            headers = {'Authorization': f"Bearer {self.api_key}"}
            body = {
                    'model':'openai/gpt-oss-120b' , 
                    'messages': [
                        {
                            'role':'user' , 
                            'content':prompt
                        }
                        ]
                    }
            response = await client.post(self.url , headers=headers , json=body)
            response.raise_for_status()

        return response.json()['choices'][0]['message']['content']
    

class Gemini(BaseProvider):
    def __init__(self,api_key):
        super().__init__(api_key)
        self.url = (
                    "https://generativelanguage.googleapis.com/v1beta/"
                    "models/gemini-2.5-flash:generateContent"
                    )

    async def fetch(self,prompt):
        async with httpx.AsyncClient(timeout=10) as client:
            headers = {
                        "Content-Type": "application/json"
                      }
            params = {'key': self.api_key}
            body = {
                    'contents':[
                        {
                            'role':'user',
                            'parts':[
                                {
                                'text':prompt
                                }
                                
                                    ]
                                }
                            ]
                    }
            response = await client.post(self.url , headers=headers , params=params, json=body)
            response.raise_for_status()

        return response.json()['candidates'][0]['content']['parts'][0]['text']


async def main():
    prompt = input('Ask the LLMs ->')
    llm1 = Groq(groq_api)
    llm2 = Gemini(gemini_api)
    async with asyncio.TaskGroup() as tg:
        groq_response = tg.create_task(llm1.fetch(prompt))
        gemini_response = tg.create_task(llm2.fetch(prompt))
    
    print('Groq ->', groq_response.result())
    print('Gemini ->' , gemini_response.result())

asyncio.run(main())

    


    
    
# asyncio.run(main())

   




