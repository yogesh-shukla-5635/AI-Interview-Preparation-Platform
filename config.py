import os
class Config:
    SECRET_KEY = "yogesh_shukla_5635"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    DATABASE = "users.db"

    UPLOAD_FOLDER = "uploads"