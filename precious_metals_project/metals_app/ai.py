import os
import requests
from django.conf import settings

class AI_V1:
    def __init__(self, model="deepseek-ai/DeepSeek-R1"):
        self.api_url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('AI_API_KEY')}"  # Используем переменную окружения
        }
        self.model = model

    def analyze_metals(self, price_dict):
        system_message = (
            "Ты специалист по драгоценным металлам. Сначала дай краткие советы на русском языке, затем на английском языке. "
            "Раздели языки строкой '==='. Формат вывода для каждого языка: Золото (XAU) Тренд: Причина: Совет: и так для всех металлов."
        )
        user_message = f"{price_dict} - это текущие цены на металлы. Проанализируй и дай рекомендации."

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)
        response_data = response.json()

        try:
            full_response = response_data['choices'][0]['message']['content']
            return full_response.split('</think>\n\n')[1] if '</think>\n\n' in full_response else full_response
        except (KeyError, IndexError) as e:
            print(f"Ошибка при обработке ответа API: {e}")
            return None
