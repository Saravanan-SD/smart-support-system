import os
from dotenv import load_dotenv

load_dotenv()

class LLMSetting:

    GROQ_API_KEY: str =os.getenv("GROQ_API_KEY")
    MODEL_NAME: str =os.getenv("MODEL_NAME")
    REDIS_URL:str = ("redis://localhost:6379/0")

setting = LLMSetting()