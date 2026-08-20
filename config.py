import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "yogesh_shukla_5635")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    DATABASE = "users.db"

    UPLOAD_FOLDER = "uploads"