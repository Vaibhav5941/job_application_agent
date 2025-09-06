from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DB_URL = os.getenv("DATABASE_URL")
