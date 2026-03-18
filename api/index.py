import sys
import os
from pathlib import Path

# Adiciona o diretório 'backend' ao sys.path para que os imports internos funcionem
# Isso resolve o erro de "ModuleNotFoundError" na Vercel
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# Importa o app FastAPI
from backend.main import app
