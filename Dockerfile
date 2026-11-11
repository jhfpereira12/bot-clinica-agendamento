FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e força flush imediato nos logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY ./app ./app

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Executa o servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
