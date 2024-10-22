# ollama连接器
import requests
import json
class AiOllamaClassifier:
    def __init__(self, api_url = "http://home.wujialei.com:11434/api/generate", model="qwen2.5:14b"):
        self.api_url = api_url
        self.model = model
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def classify_question_type(self, prompt):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response')
            return response_text.strip()
        else:
            print("Error:", response.status_code, response.text)
            return None