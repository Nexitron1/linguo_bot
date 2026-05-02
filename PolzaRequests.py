import requests
import json
from enum import Enum


class Models(Enum):
    GPT5_nano = "openai/gpt-5-nano"
 

class PolzaAI():
    def __init__(self, api_key : str):
        self.POLZA_API_KEY = api_key

    """Возвращает полный json ответ от модели по полной истории сообщений"""
    def GenerateText(self, messages, model : str):
        url = 'https://api.polza.ai/api/v1/chat/completions'
        apiModel = model
        headers = {
            "Authorization": "Bearer " + self.POLZA_API_KEY
        }
        payload = {
            "model": apiModel,
            "messages": messages         
        }
        response = None
        try:
            response = requests.post(url, json=payload, headers=headers)
        except ConnectionError as e:
            print(e)
        if response.status_code == 201 or response.status_code == 200:
            return response.json()
        else:
            print("Статус:", response.status_code)
            print("Тело ответа:", response.json())
            return None
            

    """Возвращает только текстовый ответ от модели по полной истории сообщений"""
    def SimpleGenerateText(self, messages, model : str):
        response = self.GenerateText(messages, model)
        if response:
            return response['choices'][0]['message']['content']
        else:
            return "Что-то поломалось"

    """Возвращает только текстовый ответ модели на одно сообщение без контекста"""
    def MegaSimpleGenerateText(self, userInput: str, model : str):
        response = self.SimpleGenerateText([{"role":"user", "content":userInput}], model)
        if response:
            return response
        else:
            return "Что-то поломалось"