from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    
    # MongoDB configs
    MONGO_DATABASE_HOST: str = (
        "mongodb://localhost:27017/"
    )
    MONGO_DATABASE_NAME: str = "CaptionDB"
    
settings = Config()