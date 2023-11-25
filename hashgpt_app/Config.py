"""
"""
import tiktoken

class Config:
    def __init__(self):
        self.encoding= tiktoken.get_encoding("cl100k_base")
        self.encoding= tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
        self.encoding.encode("ChatGPT is great!")