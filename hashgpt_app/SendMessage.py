"""
"""
from openai import OpenAI
from .CountTokens import CountTokens
from .ExceptionHandler import ExceptionHandler

class SendMessage():

    def send_message(self, conversation, functions, api_key, model="gpt-3.5-turbo-1106", limit=4000):
        
        try:
            self.count_tokens = CountTokens()
            self.exception_handler = ExceptionHandler()
            client = OpenAI(
                api_key=api_key,
            )
            if (self.count_tokens.num_tokens_from_messages(conversation) > limit):
                while True:
                    if (self.count_tokens.num_tokens_from_messages(conversation) > limit):
                        if (len(conversation) >= 1):
                            conversation.pop(0)
                            if (len(conversation) == 0):
                                reply = "Please reduce the length of the messages"
                                return reply
                    else:
                        break
            if (functions == 0):

                def chat_message():
                    completion = client.chat.completions.create(
                        model=model,
                        messages=conversation,
                    )
                    return [completion]
                try:
                    response = self.exception_handler.response(chat_message)
                    return response
                except:
                    return "Error!"
            else:
                def function_message():
                    response = client.chat.completions.create(
                        model=model,
                        messages=conversation,
                        functions=functions,
                        function_call="auto",
                    )
                    return response
                try:
                    response = self.exception_handler.response(function_message)
                    return response
                except:
                    return "Error!"

        except Exception as e:
            reply = "Error!"
            return reply