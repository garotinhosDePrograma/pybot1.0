from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
    GOOGLE_CX = os.getenv("GOOGLE_CX")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")