import httpx
from abc import ABC , abstractmethod
from decorators import retry , latency

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

    @latency
    @retry(times=3)    
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
    @latency
    @retry(times=3)
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

class HuggingFace(BaseProvider):
    def __init__(self,api_key):
        super().__init__(api_key)
        self.url = "https://router.huggingface.co/v1/chat/completions"

    @latency
    @retry(times=3)
    async def fetch(self,prompt):
        async with httpx.AsyncClient(timeout=10) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "openai/gpt-oss-120b",   
                "messages": [{"role": "user", "content": prompt}],
                "temperature":0.7,
                "max_tokens":200
            }
            response = await client.post(
                self.url,
                headers=headers,
                json=body
            )
            

        
            response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
