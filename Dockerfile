#
# ExposedAqui | Um projeto de scraping e análise de dados
# -----------------------------------------------------------------------------
# Copyright (C) 2025 Milena Madsen. Todos os direitos reservados.
#
# Autor: Milena Madsen
# Contacto: milena.madsen@aol.com
# GitHub: https://github.com/madmilena
#
# AVISO LEGAL:
# Este software foi desenvolvido para fins de estudo e pesquisa.
# O uso indevido deste software para violar os Termos de Serviço de qualquer
# site é estritamente proibido. A autora não se responsabiliza por
# qualquer uso indevido deste código.
#

# --- ESTÁGIO 1: A "OFICINA" (Builder) ---
# Usamos uma imagem base completa para ter acesso às ferramentas de build.
FROM python:3.11-slim AS builder

# Instalamos a nossa "caixa de ferramentas" pesada aqui.
# Necessário para compilar curl_cffi[requests] e uvicorn[standard] (uvloop, etc.).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    pkg-config \
    cargo \
    ca-certificates \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos e instalamos as dependências. O pip irá usar as toolchains acima
# para compilar os pacotes necessários (ex.: curl_cffi).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# --- ESTÁGIO 2: A "LINHA DE MONTAGEM FINAL" (Final) ---
# Começamos de novo, com um "chassi" limpo e leve.
FROM python:3.11-slim

WORKDIR /app

# Instala as libs de runtime necessárias (sem toolchain pesada)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    libffi8 \
    libcurl4 \
    && rm -rf /var/lib/apt/lists/*

# Copiamos o requirements e instalamos dependências no estágio final
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos o nosso código da aplicação (garante que o código local mais recente vai)
COPY ./app ./app

# Adiciona /usr/local/bin ao PATH só pra garantir que uvicorn será encontrado
ENV PATH="/usr/local/bin:$PATH"

# Expomos a porta e executamos
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
