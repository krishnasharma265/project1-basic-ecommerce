from dotenv import load_dotenv
import os

load_dotenv()

WRITE_DB_URL = os.getenv("WRITE_DB_URL")
READ_DB_URL = os.getenv("READ_DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)