import os
from dotenv import load_dotenv

load_dotenv()

class Setting:

    GROQ_API_KEY: str =os.getenv("GROQ_API_KEY")
    MODEL_NAME: str =os.getenv("MODEL_NAME")
    REDIS_URL:str = ("redis://localhost:6379/0")
    MONGO_URI: str = ("mongodb://localhost:27017")
    MONGO_DB: str = ("smart_support")

setting =Setting()