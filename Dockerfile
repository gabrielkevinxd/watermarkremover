FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema para o PyMuPDF
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os requirements da raiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
