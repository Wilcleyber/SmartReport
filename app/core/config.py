from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartReport"
    GROQ_API_KEY: str
    
    # Mudança crucial: dizemos que pode vir como string OU lista
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        # Se for string (como o Render envia: "url1,url2"), quebramos em lista
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                # Caso você tenha tentado o formato JSON ["url"] no painel
                import json
                return json.loads(v)
            return [i.strip() for i in v.split(",")]
        # Se já for lista, apenas retornamos
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=False # Ajuda a não dar erro se o nome estiver em minúsculo
    )

settings = Settings()