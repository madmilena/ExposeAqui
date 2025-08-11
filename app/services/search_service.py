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
A camada de Orquestração.
Este serviço coordena o trabalho entre o Coletor de Dados (Scraper) e o
Analisador de Dados (Generator) para executar a busca completa.
"""

from .scraper_strategy import ScraperStrategy, ReclameAquiScraper
from .analysis_strategy import AnalysisStrategy, DossieGenerator
from app.dtos import DossieEmpresaDTO


class SearchService:
    def __init__(self, scraper: ScraperStrategy, analyzer: AnalysisStrategy):
        self.scraper = scraper
        self.analyzer = analyzer

    def search_company(self, term: str) -> DossieEmpresaDTO:
        """
        Executa o fluxo completo de busca e análise.
        1. Chama o Scraper para coletar os dados brutos.
        2. Passa os dados brutos para o Analisador para gerar o dossiê.
        3. Retorna o dossiê final.
        """
        raw_data = self.scraper.scrape_company_data(term)
        initial_data_json = raw_data.pop("initialData")
        return self.analyzer.generate(initial_data_json, raw_data)

# Injeção de dependência "manual" para o FastAPI, instanciando as nossas implementações
def get_search_service() -> SearchService:
    scraper = ReclameAquiScraper()
    analyzer = DossieGenerator()
    return SearchService(scraper, analyzer)