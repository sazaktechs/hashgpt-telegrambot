"""
"""
import json
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from .CountTokens import CountTokens
from .SendMessage import SendMessage
from .MakeRequest import MakeRequest
from .FunctionCaller import FunctionCaller
from .FunctionCommands import FunctionCommands
class Webhook:
    def __init__(self, request):
        try:
            load_dotenv()
            self.request = request
        except:
            return Response(status=status.HTTP_200_OK)
    def after_response(self):
        try:
            if os.getenv('TOKEN'):
                self.TOKEN = os.environ['TOKEN']
            else:
                self.TOKEN = "1"
                return Response(status=status.HTTP_200_OK)
            if os.getenv('API_KEY'):
                self.API_KEY = os.environ['API_KEY']
            else:
                self.API_KEY = "1"
            self.send_message = SendMessage()
            self.make_request = MakeRequest()
            self.function_caller = FunctionCaller()
            self.count_tokens = CountTokens()
            self.function_commands = FunctionCommands()
            f = open("model.json","r")
            model = json.loads(f.read())
            model = model["model"]
            f.close()
            limit = 16000
            chat_id = self.request['message']['chat']['id']
            client = OpenAI(
                api_key = self.API_KEY,
            )
            response_message_type = self.function_commands.message_type(self.request, self.API_KEY, self.TOKEN)
            text = response_message_type[0]
            is_audio = response_message_type[1]
            chat_id = response_message_type[2]
            command_list = ["/my_key", "/start", "/help",
                            "/clear", "/read", "/google", "/dalle", "/youtube", "/gpt4","/gpt3"]
            word_list = text.split()
            intersection = False
            for i in command_list:
                if (i == word_list[0] or i == text):
                    intersection = True
            if (intersection):  
                if ("/my_key" in text):
                    if (self.API_KEY == ""):
                        reply = "Please provide an API KEY! For more information use '/help' command"
                        self.make_request.reply_request(reply, chat_id)
                        return Response(status=status.HTTP_200_OK)
                    else:
                        reply = self.API_KEY
                        self.make_request.reply_request(reply, chat_id)
                        return Response(status=status.HTTP_200_OK)
                elif (text == "/start"):
                    self.make_request.reply_request(
                        """Welcome to the chatbot powered by OpenAI's GPT-3.5 and GPT-4 APIs! I'm here to have intelligent conversations with you. Feel free to ask me any questions or chat about any topic. For more information use '/help' command.
                        """, chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/gpt4"):
                    text = "How to use: /gpt4 gpt-4"
                    self.make_request.reply_request(text, chat_id, parse_mode = "HTML")
                elif (text == "/gpt3"):
                    text = "How to use: /gpt3 gpt-3.5"
                    self.make_request.reply_request(text, chat_id, parse_mode = "HTML")
                elif ("/gpt4" in text and len(text) > 5):
                    try:
                        f = open("model.json","w")
                        f.write(json.dumps({"model":"gpt-4-1106-preview"}))
                        f.close()
                        self.make_request.reply_request(
                        """Your text-model changed to gpt-4-1106-preview
                        """, chat_id)
                    except:
                        self.make_request.reply_request(
                        """Error!
                        """, chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif ("/gpt3" in text and len(text) > 5):
                    try:
                        f = open("model.json","w")
                        f.write(json.dumps({"model":"gpt-3.5-turbo-1106"}))
                        f.close()
                        self.make_request.reply_request(
                        """Your text-model changed to gpt-3.5-turbo-1106
                        """, chat_id)
                    except:
                        self.make_request.reply_request(
                        """Error!
                        """, chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/help"):
                    text = """
    Hello! I am a helpful assistant! You can ask me anything within my capabilities. I'm here to help!
Additionally, you can use helpful commands! To display all available commands, simply press '/'. From the list of commands, you can select the one you want more information about.
Please make sure you have provided the API key! If you haven't yet provided an API key, please open the .env file and add a new key-value pair with the key name 'API_KEY' and the corresponding API key as the value, like this:
API_KEY=your_actual_api_key_here
Make sure to save the changes once you've added the key.
If you are uncertain about your API Key, please visit your <a href="https://platform.openai.com/account/api-keys">API Keys page</a> for more information.
    """
                    self.make_request.reply_request(text, chat_id, parse_mode = "HTML")
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/clear"):
                    response = self.function_commands.clear(chat_id)
                elif (text == "/read"):
                    self.make_request.reply_request(
                        'How to use: /read <url> <prompt>\n\nExample: /read https://en.wikipedia.org/wiki/Alan_Turing Use bullet points to explain what this article is about. Make sure each point is no longer than 10 words long. At the end write a summary about the paper in no more than 300 words.', chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/google"):
                    self.make_request.reply_request(
                        'How to use: /google <prompt>\n\nExample: /google upcoming movies in 2024', chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif ("/read" in text or "/google" in text):
                    api_key = self.API_KEY
                    response = self.function_commands.read(chat_id, text, api_key, model)
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/youtube"):
                    self.make_request.reply_request(
                        'How to use: /youtube <url> <prompt>\n\nExample: /youtube https://youtu.be/7SWvDHvWXok Summarize this video in five bullet points.\n\n', chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif ("/youtube" in text):
                    api_key = self.API_KEY
                    response = self.function_commands.youtube(chat_id, text, api_key, model)
                    return Response(status=status.HTTP_200_OK)
                elif (text == "/dalle"):
                    self.make_request.reply_request(
                        'How to use: /dalle <image description> <image size: ["256x256", "512x512", "1024x1024"]>\n\nExample: /dalle a white siamese cat 1024x1024', chat_id)
                    return Response(status=status.HTTP_200_OK)
                elif ("/dalle" in text):
                    client = OpenAI(
                        api_key = self.API_KEY,
                    )
                    api_key = self.API_KEY
                    self.function_caller.functions(chat_id, text, api_key, model)
                    return Response(status=status.HTTP_200_OK)
                else:
                    self.make_request.reply_request(
                        'Provide command correctly!\n\tExample: /help', chat_id)
                    return Response(status=status.HTTP_200_OK)
            elif (text == "/"):
                self.make_request.reply_request(
                    'Provide command correctly!\n\tExample: /help', chat_id)
                return Response(status=status.HTTP_200_OK)
            else:
                api_key = self.API_KEY
                f = open("conversations.json", "r")
                conversation = json.loads(f.read())
                f.close()
                message = {"role": "user", "content": str(text)}
                conversation.append(message)
                try:
                    completion = self.send_message.send_message(
                        conversation=conversation, functions=0, api_key = api_key, model = model, limit = limit)
                except Exception as e:
                    pass
                if (type(completion) == list):
                    completion = completion[0]
                    response = self.make_request.reply_request(
                        completion.choices[0].message.content, chat_id)
                else:
                    reply = completion
                    self.make_request.reply_request(reply, chat_id)
                    return Response(status=status.HTTP_200_OK)
                try:
                    if (is_audio):
                        speech_file_path = "./speech.mp3"
                        response = client.audio.speech.create(
                        model="tts-1",
                        voice="onyx",
                        input=completion.choices[0].message.content
                        )
                        response.stream_to_file(speech_file_path)
                        url = f'https://api.telegram.org/bot{self.TOKEN}/sendAudio'
                        payload = {
                            'chat_id': str(chat_id),
                        }
                        files = {
                            'audio': open("./speech.mp3", "rb") 
                        }
                        response = requests.post(url, data=payload, files=files)
                        if response.status_code == 200:
                            try:
                                os.remove(speech_file_path)
                            except Exception as e:
                                pass
                        else:
                            pass
                        response = response.status_code
                    if (response == 200):
                        message = {"role":"assistant", "content": completion.choices[0].message.content}
                        conversation.append(message)
                        f = open("conversations.json", "w")
                        f.write(json.dumps(conversation))
                        f.close()
                except Exception as e:
                    self.make_request.reply_request("Error!", chat_id)
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_200_OK)