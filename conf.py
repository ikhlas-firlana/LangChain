import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

PROXYCURL_TOKEN = os.getenv("PROXYCURL_API")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TAVILY_TOKEN = os.getenv("TAVILY_API_KEY")


