from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # O Pydantic procura automaticamente essas chaves no seu arquivo .env
    PROJECT_NAME: str = "SmartReport"
    GROQ_API_KEY: str
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # Configuração para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instância global para ser importada nos outros módulos
settings = Settings()