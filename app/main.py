import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.endpoints import router as api_router

load_dotenv()

app = FastAPI(title="SmartReport API", version="1.0.0")

# Garante a pasta de uploads no início
os.makedirs("uploads", exist_ok=True)

# Configuração de CORS
origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Aqui conectamos as rotas que estão no arquivo de endpoints
app.include_router(api_router)

@app.get("/")
async def health_check():
    return {"status": "online", "message": "SmartReport Server Running"}