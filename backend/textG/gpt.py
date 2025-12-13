from openai import OpenAI
from typing import Dict, Optional
from django.conf import settings


class GPTClient:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        api_key = "sk-proj-" + api_key[:3:-1] if api_key.startswith('gpt:') else api_key
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history = {}
    
    def send_message(self,
                     message: str,
                     session_id: str = "default") -> str:
        """
        Базовая функция для отправки сообщения
        """
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        system_prompt = """Ты специалист по созданию поздравлений и сценариев для видео-поздравлений.
        Пользователь будет просить тебя генерировать текст поздравлений или идеи для видео.
        Отвечай креативно и учитывай контекст предыдущих сообщений в диалоге."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        messages.extend(self.conversation_history[session_id])
        
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        response_text = response.choices[0].message.content
        
        self.conversation_history[session_id].append({"role": "user", "content": message})
        self.conversation_history[session_id].append({"role": "assistant", "content": response_text})
        
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
        
        return response_text
    
    def regenerate_text(self,
                        message: str,
                        session_id: str = "default") -> str:
        """
        Функция для переделки текста с учетом контекста
        message должен содержать и текст, и инструкции
        """
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        system_prompt = """Ты помощник для редактирования текстов.
        Пользователь будет отправлять тебе текст и инструкции, как его изменить.
        Твоя задача - переработать текст согласно инструкциям, сохраняя основную идею."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        messages.extend(self.conversation_history[session_id])
        
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        response_text = response.choices[0].message.content
        
        self.conversation_history[session_id].append({"role": "user", "content": message})
        self.conversation_history[session_id].append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def clear_history(self, session_id: Optional[str] = None):
        """Очищает историю сообщений"""
        if session_id:
            if session_id in self.conversation_history:
                del self.conversation_history[session_id]
        else:
            self.conversation_history.clear()