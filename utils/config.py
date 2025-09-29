from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DB_URL = os.getenv("DATABASE_URL")

# Cookie/session settings for Streamlit
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "jaa_session")
SESSION_TTL_HOURS = int(os.getenv("SESSION_TTL_HOURS", "72"))