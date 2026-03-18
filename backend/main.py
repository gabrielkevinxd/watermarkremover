import sys
from pathlib import Path
# Add current directory to path if running from root (Vercel)
sys.path.append(str(Path(__file__).parent.resolve()))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# CORS Rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since separating Frontend and Backend, make sure to allow CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Implementation
app.include_router(api_router, prefix="/api")

# Serve o Frontend - Adicionado para facilitar o deploy no Docker/Coolify
from fastapi.staticfiles import StaticFiles
import os

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    # Fallback para o caso de estar sendo rodado de outra pasta (root)
    frontend_path_root = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_path_root):
        app.mount("/", StaticFiles(directory=frontend_path_root, html=True), name="frontend")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notebooklm-watermark-remover"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
