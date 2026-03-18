from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "NotebookLM Watermark Remover API"
    PROJECT_DESCRIPTION: str = "API structure for the NotebookLM PDF Watermark Remover"
    PROJECT_VERSION: str = "1.0.0"
    
    # Storage settings
    import os
    import platform
    is_vercel = os.environ.get("VERCEL") == "1"
    
    STORAGE_DIR: Path = Path("/tmp/temp") if (is_vercel or platform.system() != "Windows") else Path("./temp")
    UPLOAD_DIR: Path = STORAGE_DIR / "uploads"
    OUTPUT_DIR: Path = STORAGE_DIR / "outputs"
    
    def setup_dirs(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.setup_dirs()
