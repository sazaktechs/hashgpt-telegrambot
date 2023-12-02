"""
"""
import json
import requests
import io
import os
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .ResponseThen import ResponseThen
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
from .CountTokens import CountTokens
from .MakeRequest import MakeRequest
from .Config import Config
from .SendMessage import SendMessage
from .FunctionCaller import FunctionCaller

class FunctionCommands:

    def __init__(self):
        self.count_tokens = CountTokens()
        self.config = Config()
        self.make_request = MakeRequest()
        self.send_message = SendMessage()
        self.function_caller = FunctionCaller()

    def youtube(self, chat_id, text, api_key, model):
        response = self.function_caller.functions(chat_id, text, api_key, model)
        if (response == 0):
            self.make_request.reply_request("Error!", chat_id)
        else:
            try:
                r = self.make_request.reply_request(
                    response[1].choices[0].message.content, chat_id)
                if (r == 200):
                    f = open("conversations.json", "r")
                    conversation = json.loads(f.read())
                    f.close()
                    f = open("conversations.json", "w")
                    conversation.append({"role": "user", "content": text})
                    conversation.append(response[0])
                    f.write(json.dumps(conversation))
                    f.close()
            except Exception as e:
                self.make_request.reply_request("Error!", chat_id)
        return Response(status=status.HTTP_200_OK)
    
    def read(self, chat_id, text, api_key, model):
        response = self.function_caller.functions(chat_id, text, api_key, model)
        if (response == 0):
            self.make_request.reply_request(
                "Error! Content could not be retrieved", chat_id)
        elif (response == "command" and "/read" in text):
            self.make_request.reply_request(
                "Please, provide command correctly\n Example: /read <url> <prompt>", chat_id)
        elif (response == "command" and "/google" in text):
            self.make_request.reply_request(
                "Please, provide command correctly\n Example: /google <prompt>", chat_id)
        else:
            try:
                r = self.make_request.reply_request(
                    response[1].choices[0].message.content, chat_id)
                if (r == 200):
                    f = open("conversations.json", "r")
                    conversation = json.loads(f.read())
                    f.close()
                    f = open("conversations.json", "w")
                    conversation.append({"role": "user", "content": text})
                    conversation.append(response[0])
                    f.write(json.dumps(conversation))
                    f.close()
            except Exception as e:
                self.make_request.reply_request("Error!", chat_id)
        return Response(status=status.HTTP_200_OK)

    def clear(self, chat_id):

        f = open("conversations.json", "w")
        f.write(json.dumps([{"role": "system", "content": "You are a helpful assistant."}]))
        f.close()
        self.make_request.reply_request('Session restarted!', chat_id)
        return Response(status=status.HTTP_200_OK)
    
    def message_type(self, request, api_key, TOKEN):

        supported_types = ['text', 'audio', 'document', 'photo', 'voice']
        for message_type in supported_types:
            if request['message'].get(message_type):
                type = message_type
                value = request['message'][message_type]
                if('caption' in request['message']):
                    caption = request['message']['caption']
                else:
                    caption = ""
                break
            else:
                type = False
                value = False

        is_audio = False

        client = OpenAI(
            api_key = api_key,
        )

        chat_id = request['message']['chat']['id']

        if(type == 'text'):
            text = request['message']['text']
            
        
        elif(type == 'document'):
            
            url = f"https://api.telegram.org/bot" + TOKEN + "/getFile"
            payload = {
                'file_id': value['file_id'],
            }
            response = requests.get(url, json=payload)
            response = json.loads(response.content)
            file_path = response['result']['file_path']
            url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            response = requests.get(url)
            
            if(".pdf" in url):
                on_fly_mem_obj = io.BytesIO(response.content)
                pdf_file = PdfReader(on_fly_mem_obj)
                text = ""
                number_of_pages = len(pdf_file.pages)
                for i in range(0, number_of_pages):
                    page = pdf_file.pages[i]
                    text = text + page.extract_text()
                response = text
            else:
                response = response.content.decode('UTF-8')
            
            text = caption + ' """' + response + '"""'
            
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": str(text)}])
            
            
            if (num_tokens > 16000):
                limit = 16000
                text_list = text.split(".")
                
                num = int(num_tokens / 16000) + 1
                
                text = r""
                
                counter = 0
                for i in text_list:
                    if (counter < 10):
                        text = text + str(i) + " "
                        counter += 1
                        if (counter >= 10):
                            counter += num * 10
                    elif (counter >= 10):
                        counter -= 1
                        if (counter == 10):
                            counter = 0
                num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": str(text)}])
                

        elif(type == 'audio' or type == 'voice'):
            
            url = f"https://api.telegram.org/bot" + TOKEN + "/getFile"
            payload = {
                'file_id': value['file_id'],
            }
            response = requests.get(url, json=payload)
            response = json.loads(response.content)
            file_path = response['result']['file_path']
            url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            response = requests.get(url)
            file_name = file_path.split('.')
            file_name = value['file_unique_id'] + '.' + file_name[len(file_name) - 1]
            with open(file_name, 'wb') as file:
                file.write(response.content)
            audio_file= open(file_name, "rb")
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            is_audio = True
            text = str(transcript.text)
            try:
                os.remove("./" + str(file_name))
                
            except FileNotFoundError:
                
            except PermissionError:
                

        return [text, is_audio, chat_id]
