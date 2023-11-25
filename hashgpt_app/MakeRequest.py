"""
"""
import requests
import os
from dotenv import load_dotenv
from .SendMessage import SendMessage
from .ExceptionHandler import ExceptionHandler

class MakeRequest:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.environ['TOKEN']
        self.send_message = SendMessage()
        self.exception_handler = ExceptionHandler()
    
    def reply_request(self, reply, chat_id, parse_mode = ""):
        url = f"https://api.telegram.org/bot" + self.TOKEN + "/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': reply,
            'parse_mode': parse_mode
        }
        response = requests.post(url, json=payload)
        return response.status_code