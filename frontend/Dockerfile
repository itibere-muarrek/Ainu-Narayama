FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar usuário não-root
RUN useradd -m streamlit && chown -R streamlit:streamlit /app
USER streamlit

# Expor porta
EXPOSE 8501

# Health check
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1

# Comando de inicialização
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
