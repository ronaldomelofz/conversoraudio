# 🎯 TRANSCRITOR AVANÇADO - API FLASK
# Dockerfile para containerização
# Inspirado em TranscreveAPI mas MUITO mais poderoso!

FROM python:3.11-slim

# Metadados
LABEL maintainer="Sistema Avançado de Transcrição"
LABEL version="3.0"
LABEL description="API Flask avançada para transcrição com Whisper - Inspirado em TranscreveAPI"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=transcritor_api_flask.py
ENV FLASK_ENV=production

# Instala dependências do sistema (SEM FFmpeg - nossa vantagem!)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia requirements primeiro (cache layer)
COPY requirements_api.txt .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_api.txt

# Copia código da aplicação
COPY transcritor_api_flask.py .
COPY config.example config

# Cria diretórios necessários
RUN mkdir -p /app/transcricoes /app/uploads

# Exposição da porta
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando padrão
CMD ["python", "transcritor_api_flask.py"]

# ===== INSTRUÇÕES DE USO =====
# 
# 1. BUILD:
#    docker build -t transcritor-api .
#
# 2. RUN:
#    docker run -p 5000:5000 transcritor-api
#
# 3. VOLUME (opcional para persistir transcriações):
#    docker run -p 5000:5000 -v $(pwd)/transcricoes:/app/transcricoes transcritor-api
#
# 4. ENVIRONMENT (opcional):
#    docker run -p 5000:5000 -e FLASK_ENV=development transcritor-api
#
# 5. DOCKER COMPOSE (recomendado para produção):
#    Veja docker-compose.yml
#
# 🚀 VANTAGENS sobre TranscreveAPI original:
#    ✅ Container mais leve (sem FFmpeg)
#    ✅ 100% offline (sem APIs externas)
#    ✅ 5 modelos Whisper
#    ✅ Interface web incluída
#    ✅ Compatibilidade total 