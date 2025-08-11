#
# ExposeAqui | Um projeto de scraping e análise de dados do ReclameAqui
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
Define a estratégia e a implementação para a coleta de dados (Scraping).
Esta é a camada responsável por toda a comunicação de rede e pela imitação
de um navegador para contornar proteções como o Cloudflare.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from curl_cffi import requests
from app.dtos import CompanyDTO


class ScraperStrategy(ABC):
    """Interface que define o contrato para qualquer coletor de dados."""

    @abstractmethod
    def scrape_company_data(self, term: str) -> Dict[str, Any]:
        pass


class ReclameAquiScraper(ScraperStrategy):
    """
    Implementação da estratégia de scraping para o site ExposeAqui Aqui.
    Utiliza um cliente HTTP com capacidade de imitar um navegador (curl_cffi)
    para fazer as chamadas de API diretamente, sem a necessidade de um navegador.
    """
    BASE_URL = "https://www.reclameaqui.com.br"
    API_SEARCH_URL = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1"
    API_SITE_URL = "https://iosite.reclameaqui.com.br/raichu-io-site-v1"

    def __init__(self):
        """Inicializa a sessão de requisições, configurando-a para imitar um navegador."""
        self.session = requests.Session(impersonate="chrome110", timeout=30)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.reclameaqui.com.br",
            "Referer": "https://www.reclameaqui.com.br/",
        }
        print("INFO:     ExposedAqui iniciado.")

    def scrape_company_data(self, term: str) -> Dict[str, Any]:
        """
        Executa o fluxo completo de scraping:
        1. Estabelece uma sessão válida para passar pelo Cloudflare.
        2. Realiza a busca inicial para encontrar a empresa.
        3. Chama as APIs de perfil para coletar os dados detalhados.
        Retorna um dicionário com os dados brutos de cada API capturada.
        """
        try:
            # Etapa 1: Estabelecer sessão e obter cookies de desafio, se necessário
            # print(f">>> A estabelecer sessão com {self.BASE_URL}...")
            self.session.get(self.BASE_URL, headers=self.headers)
            # print(">>> Sessão estabelecida com sucesso.")

            # Etapa 2: Fazer a busca inicial pela API
            # print(f">>> A procurar pelo termo: {term}")
            search_url = f"{self.API_SEARCH_URL}/companies/modern-search/{term}"
            response = self.session.get(search_url, headers=self.headers)
            response.raise_for_status()

            search_data = response.json()
            if not search_data.get("companies"):
                raise ValueError(f"WARN:     Nenhuma empresa encontrada para o termo: {term}")

            first_company = CompanyDTO.model_validate(search_data["companies"][0])
            company_id = first_company.id
            shortname = first_company.shortname
            print(f"INFO:     Empresa encontrada: {first_company.fantasy_name} (ID: {company_id})")

            # Etapa 3: Chamar as APIs de perfil diretamente
            raw_data_responses = {"initialData": first_company.model_dump_json(by_alias=True)}

            api_calls = {
                "profile": f"{self.API_SITE_URL}/company/shortname/{shortname}",
                "mainProblems": f"{self.API_SEARCH_URL}/query/companyMainProblems/{company_id}",
                "problems6Months": f"{self.API_SEARCH_URL}/query/companyPerformanceProblems6Months/{company_id}",
                "indexEvolution": f"{self.API_SITE_URL}/company/indexevolution/{company_id}"
            }

            for key, url in api_calls.items():
                try:
                    # print(f">>> A chamar API: {key}")
                    resp = self.session.get(url, headers=self.headers)
                    if resp.ok:
                        raw_data_responses[key] = resp.text
                        # print(f"--- Sucesso ao obter dados de {key}")
                    else:
                        print(f"WARN:     Falha ao obter dados de {key}. Status: {resp.status_code}")
                except Exception as e:
                    print(f"WARN:     Erro ao chamar a API {key}: {e}")

            return raw_data_responses

        except Exception as e:
            print(f"ERROR:     Erro fatal durante o scraping: {e}")
            raise e