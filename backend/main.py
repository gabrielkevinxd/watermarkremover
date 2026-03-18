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

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notebooklm-watermark-remover"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
