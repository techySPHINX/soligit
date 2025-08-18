
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY")
    WEAVIATE_ENVIRONMENT: str = os.getenv("WEAVIATE_ENVIRONMENT", "asia-southeast1-gcp-free")
    WEAVIATE_INDEX: str = os.getenv("WEAVIATE_INDEX", "chatpdf")
    GITHUB_PERSONAL_ACCESS_TOKEN: str = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    AAI_TOKEN: str = os.getenv("AAI_TOKEN")

    class Config:
        env_file = ".env"

settings = Settings()
