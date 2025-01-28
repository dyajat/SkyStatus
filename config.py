import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")