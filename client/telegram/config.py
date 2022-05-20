from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

# CONFIG
API_TOKEN = os.getenv('API_TOKEN')
REDIS_URL = os.getenv('REDIS_URL')
ADMIN_ID = os.getenv('ADMIN_ID')

APP_NAME = "SmartHeart"