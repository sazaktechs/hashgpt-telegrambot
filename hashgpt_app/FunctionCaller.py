"""
"""
import json
from openai import OpenAI
import requests
import re
import io
from pypdf import PdfReader
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
from .CountTokens import CountTokens
from .MakeRequest import MakeRequest
from .Config import Config
from .SendMessage import SendMessage

class FunctionCaller:

    def functions(self, chat_id, text, api_key, model):
        self.count_tokens = CountTokens()
        self.config = Config()
        self.make_request = MakeRequest()
        self.send_message = SendMessage()
        client = OpenAI(
            api_key=api_key,
        )
        model = model
        text = str(text)
        word_list = text.split()
        search_query = word_list[1:]
        search_query = "+".join(search_query)
        if not (word_list[0] == '/archive' or word_list[0] == '/read' or word_list[0] == '/youtube' or word_list[0] == '/google' or word_list[0] == '/dalle'):
            if not("/google" in text):
                self.make_request.reply_request(
                    "Please provide command correctly!\n/read <url> <prompt>", chat_id)
                return Response(status=status.HTTP_200_OK)
            self.make_request.reply_request(
                    "Please provide command correctly!\n/google <prompt>", chat_id)
            return Response(status=status.HTTP_200_OK)
        url = word_list[1]

        def get_content(url):
            """Get the current weather in a given location"""
            try:
                response = requests.get(url)
                webpage_content = response.content
                soup = BeautifulSoup(webpage_content, 'html.parser')
                if (response.status_code != 200):
                    return 0
            except Exception as e:
                return 0
            if(".pdf" in url):
                on_fly_mem_obj = io.BytesIO(response.content)
                pdf_file = PdfReader(on_fly_mem_obj)
                text = ""
                number_of_pages = len(pdf_file.pages)
                for i in range(0, number_of_pages):
                    page = pdf_file.pages[i]
                    text = text + page.extract_text()
                website_text = text
            else:
                if ("google.com" in url):
                        element = soup.find()
                        website_text = element.get_text()
                else:
                    element = soup.find("body")
                    website_text = element.get_text()
            website_text = re.sub(r"\s{2,}", " ", website_text)
            website_text = website_text.replace('\n', '')
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": str(website_text)}])
            if (num_tokens > 16000):
                website_text_list = website_text.split(".")
                num = int(num_tokens / 16000) + 1
                website_text = r""
                counter = 0
                for i in website_text_list:
                    if (counter < 10):
                        website_text = website_text + str(i) + " "
                        counter += 1
                        if (counter >= 10):
                            counter += num * 10
                    elif (counter >= 10):
                        counter -= 1
                        if (counter == 10):
                            counter = 0
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": website_text}])
            url_info = {
                "url": url,
                "content": website_text,  
                "model": model
            }
            self.make_request.reply_request("Content read!", chat_id)
            return json.dumps(url_info)
        
        def get_google_results(url):
            
            try:
                response = requests.get(url)
                webpage_content = response.content
                soup = BeautifulSoup(webpage_content, 'html.parser')
                if (response.status_code != 200):
                    return 0
            except Exception as e:
                return 0
            if(".pdf" in url):
                on_fly_mem_obj = io.BytesIO(response.content)
                pdf_file = PdfReader(on_fly_mem_obj)
                text = ""
                number_of_pages = len(pdf_file.pages)
                for i in range(0, number_of_pages):
                    page = pdf_file.pages[i]
                    text = text + page.extract_text()
                website_text = text
            else:
                element = soup.find("body")
                website_text = element.get_text()
            website_text = re.sub(r"\s{2,}", " ", website_text)
            website_text = website_text.replace('\n', '')
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": str(website_text)}])
            if (num_tokens > 16000):
                website_text_list = website_text.split(".")
                num = int(num_tokens / 16000) + 1
                website_text = r""
                counter = 0
                for i in website_text_list:
                    if (counter < 10):
                        website_text = website_text + str(i) + " "
                        counter += 1
                        if (counter >= 10):
                            counter += num * 10
                    elif (counter >= 10):
                        counter -= 1
                        if (counter == 10):
                            counter = 0
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": website_text}])
            url_info = {
                "url": url,
                "content": website_text,  
                "model": model
            }
            self.make_request.reply_request("Content read!", chat_id)
            return json.dumps(url_info)
        
        def get_transcript(url):
            """Get the transcript of youtube video from the given url"""
            language_codes = [
                'en', 'tr', 'af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'eu', 'be', 'bho', 'bs', 'bg', 'my',
                'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'eo', 'et', 'ee',
                'fil', 'fi', 'fr', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn',
                'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'kri', 'ku', 'ky',
                'lo', 'la', 'lv', 'ln', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'nso',
                'no', 'ny', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'sr',
                'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th',
                'ti', 'ts', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'fy', 'xh', 'yi', 'yo', 'zu'
            ]
            try:
                id = extract.video_id(url)
            except Exception as e:
                reply = "Error! No video found\nMake sure to write the message in this format:\n/youtube <url> <message>"
                self.make_request.reply_request(reply, chat_id)
                return 0
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(id)
                transcript = transcript_list.find_manually_created_transcript(
                    language_codes)
            except Exception as e:
                try:
                    transcript = transcript_list.find_generated_transcript(
                        language_codes)
                except Exception as e:
                    reply = "Error! No transcript found"
                    self.make_request.reply_request(reply, chat_id)
                    return 0
            transcript = YouTubeTranscriptApi.get_transcript(
                id, [transcript.language_code])
            video_text = r""
            for i in transcript:
                video_text = video_text + str(i['text']) + " "
            video_text = re.sub(r"\s{2,}", " ", video_text)
            video_text = video_text.replace('\n', '')
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": video_text}])
            if (num_tokens > 16000):
                num = int(num_tokens / 16000) + 1
                video_text = r""
                counter = 0
                for i in transcript:
                    if (counter < 10):
                        video_text = video_text + str(i['text']) + " "
                        counter += 1
                        if (counter >= 10):
                            counter = num * 10
                    elif (counter >= 10):
                        counter -= 1
                        if (counter == 10):
                            counter = 0
            video_text = re.sub(r"\s{2,}", " ", video_text)
            video_text = video_text.replace('\n', '')
            num_tokens = self.count_tokens.num_tokens_from_messages(
                [{"text": video_text}])
            info = {
                "transcript": video_text,
                "model": model
            }
            num_tokens = self.count_tokens.num_tokens_from_messages([info])
            self.make_request.reply_request("Watched the video!", chat_id)
            return (json.dumps(info))
        
        def get_image_prompt(prompt, size):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    quality="standard",
                )
                image_url = response.data[0].url
                self.make_request.reply_request(image_url, chat_id)
                return 0
            except Exception as e:
                self.make_request.reply_request("Error! Image could not created", chat_id)
                return 0
        if ("/read" in word_list or "/google" in word_list):
            messages = [{"role": "user", "content": str(text)}]
            functions = [
                {
                    "name": "get_content",
                    "description": "Get the content of website from the given url",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url of a website, e.g. https://www.python.org/",
                            },
                        },
                        "required": ["url", "prompt"],
                    },
                },
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call="auto",  
            )
            response_message = response.choices[0].message
            function_call = response_message.function_call
            if function_call:
                available_functions = {
                    "get_content": get_content,
                    "get_google_results": get_google_results,
                }  
                function_name = response_message.function_call.name
                fuction_to_call = available_functions[function_name]
                function_args = json.loads(
                    response_message.function_call.arguments)
                function_response = fuction_to_call(
                    url=function_args.get("url"),
                )
                if(function_response == 0):
                    return 0
                response_function = json.loads(function_response)
                model = response_function['model']
                function_response = function_response.encode().decode("unicode-escape")
                function_response = function_response.replace("\'", "")
                function_response = function_response.replace("\n", "")
                num_tokens = self.count_tokens.num_tokens_from_messages(
                    [{"text": str(function_response)}])
                messages.append(response_message)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  
                try:
                    second_response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                    )  
                except Exception as e:
                    return 0
                return [{
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                        },
                        second_response]
            else:
                return "command"
        elif ("/youtube" in word_list):
            messages = [{"role": "user", "content": str(text)}]
            functions = [
                {
                    "name": "get_transcript",
                    "description": "Get the transcript of youtube video from the given url",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url of the youtube video, e.g. https://www.youtube.com/watch?v=Y7dpJ0oseIA",
                            },
                        },
                        "required": ["url"],
                    },
                },
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call="auto",  
            )
            response_message = response.choices[0].message
            function_call = response_message.function_call
            if function_call:
                available_functions = {
                    "get_transcript": get_transcript,
                }  
                function_name = response_message.function_call.name
                fuction_to_call = available_functions[function_name]
                function_args = json.loads(
                    response_message.function_call.arguments)
                function_response = fuction_to_call(
                    url=function_args.get("url"),
                )
                response_function = json.loads(function_response)
                model = response_function['model']
                function_response = function_response.encode().decode("unicode-escape")
                function_response = function_response.replace("\'", "'")
                messages.append(response_message)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  
                try:
                    second_response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                    )  
                except Exception as e:
                    return 0

                return [{
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                        },
                        second_response]
            else:
                return response_message
        elif ("/dalle" in word_list):
            messages = [{"role": "user", "content": str(text)}]
            functions = [
                {
                    "name": "get_image_prompt",
                    "description": "Get the prompt for the client.DALL·E image",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt for the DALL·E, e.g. a white siamese cat",
                            },
                            "size": {
                                "type": "string",
                                "description": "The size of the image for the DALL·E, e.g. 1024x1024",
                            },
                        },
                        "required": ["prompt", "size"],
                    },
                }
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call="auto",  
            )
            response_message = response.choices[0].message
            function_call = response_message.function_call
            if function_call:
                available_functions = {
                    "get_image_prompt": get_image_prompt,
                }  
                function_name = response_message.function_call.name
                fuction_to_call = available_functions[function_name]
                function_args = json.loads(
                    response_message.function_call.arguments)
                try:
                    function_response = fuction_to_call(
                        prompt=function_args.get("prompt"),
                        size=function_args.get("size"),
                    )
                except Exception as e:
                    self.make_request.reply_request('Error!', chat_id)
                return Response(status=status.HTTP_200_OK)
            else:
                return response_message
        return Response(status=status.HTTP_200_OK)
