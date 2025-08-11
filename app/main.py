#
# ExposeAqui | Um projeto de scraping e análise de dados
# -----------------------------------------------------------------------------
# Copyright (C) 2025 Milena Madsen. Todos os direitos reservados.
#
# Autor: Milena Madsen
# Contacto: milena.madsen@aol.com
# GitHub: https://github.com/madmilena
#
# AVISO LEGAL:
# Este software foi desenvolvido para fins de estudo e pesquisa. O seu objetivo
# é demonstrar técnicas de coleta e análise de dados de fontes públicas.
# O uso indevido deste software para violar os Termos de Serviço de qualquer
# site, incluindo, mas não se limitando a reclameaqui.com.br e cloudflare.com,
# é estritamente proibido.
#
# A autora não se responsabiliza por qualquer uso indevido deste código ou por
# quaisquer consequências legais ou financeiras decorrentes de tal uso.
#

"""
Ponto de entrada principal da aplicação web (API).
Define os endpoints, recebe as requisições HTTP e as delega para a camada de serviço.
Inclui um "starter" para facilitar a execução em modo de desenvolvimento.
"""

import uvicorn # Importamos o uvicorn para o podermos iniciar a partir do código
from fastapi import FastAPI, Depends, HTTPException
from app.services.search_service import SearchService, get_search_service
from app.dtos import DossieEmpresaDTO

app = FastAPI(
    title="ExposeAqui",
    description="API para scraping e análise de reputação de empresas no ExposeAqui Aqui.",
    version="2.0.0-FINAL"
)

@app.get(
    "/search/{term}",
    response_model=DossieEmpresaDTO,
    response_model_by_alias=True,
    summary="Busca e analisa uma empresa",
    description="Recebe um CNPJ ou nome de empresa, realiza o scraping completo e retorna um dossiê 360°."
)
def search(term: str, service: SearchService = Depends(get_search_service)):
    try:
        return service.search_company(term)
    except Exception as e:
        print(f"Erro na rota de busca: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", include_in_schema=False)
def root():
    return {"message": "ExposeAqui está no ar!"}


# =========================================================================
# STARTER DA APLICAÇÃO
# =========================================================================
# Este bloco só é executado quando você roda o ficheiro diretamente com:
# python3 app/main.py
if __name__ == "__main__":
    print(">>> A iniciar a aplicação em modo de desenvolvimento...")
    uvicorn.run(
        "app.main:app", # O caminho para a sua instância do FastAPI
        host="127.0.0.1",
        port=8000,
        reload=True # Ativa o hot-reload, muito útil para desenvolvimento
    )