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
Define a estratégia e a implementação para a análise e transformação dos dados.
Esta camada é o "Chef de Cozinha": recebe os dados brutos do Scraper e os
transforma no Dossiê 360° final, aplicando as regras de negócio.
"""

from abc import ABC, abstractmethod
from app.dtos import *
import json


class AnalysisStrategy(ABC):
    """Interface que define o contrato para qualquer analisador de dados."""

    @abstractmethod
    def generate(self, initial_data_json: str, raw_data: Dict[str, str]) -> DossieEmpresaDTO:
        pass


class DossieGenerator(AnalysisStrategy):
    """
    Implementação da estratégia de análise. Sabe como processar os JSONs brutos
    do ExposeAqui e transformá-los num dossiê estruturado e de alto valor.
    """

    def generate(self, initial_data_json: str, raw_data: Dict[str, str]) -> DossieEmpresaDTO:
        """
        Método público que recebe os dados brutos, converte-os e chama a
        lógica de análise principal.
        """
        initial_data = CompanyDTO.model_validate_json(initial_data_json)
        profile = json.loads(raw_data.get("profile")) if "profile" in raw_data else None
        main_problems = json.loads(raw_data.get("mainProblems")) if "mainProblems" in raw_data else None
        problems_6_months = json.loads(raw_data.get("problems6Months")) if "problems6Months" in raw_data else None
        evolution = json.loads(raw_data.get("indexEvolution")) if "indexEvolution" in raw_data else None
        return self._generate_dossie(initial_data, profile, main_problems, problems_6_months, evolution)

    def _generate_dossie(self, initial_data: CompanyDTO, profile: Dict, main_problems: Dict, problems_6_months: Dict,
                         evolution: Dict) -> DossieEmpresaDTO:
        """
        O coração da lógica de negócio. Constrói o dossiê final de forma
        adaptativa, tratando os diferentes tipos de empresa (verificada vs. não verificada).
        """
        identificacao: IdentificacaoDTO
        dossie: DossieEmpresaDTO

        if profile:
            # --- Lógica para empresas com API de perfil (geralmente as verificadas) ---
            ident_data = {
                "idReclameAqui": profile.get("id"),
                "razaoSocial": profile.get("companyName"),
                "nomeFantasia": profile.get("fantasyName"),
                "dataCadastroPlataforma": profile.get("created"),
                "endereco": profile.get("address"),
                "cnpj": (profile.get("documents") or [{}])[0].get("number")
            }
            identificacao = IdentificacaoDTO.model_validate(ident_data)
            dossie = DossieEmpresaDTO(identificacao=identificacao)

            operacional_data = {
                "sitePrincipal": profile.get("urlSite"),
                "segmentoPrincipal": profile.get("mainSegment", {}).get("title"),
                "segmentosSecundarios": [seg.get("title") for seg in profile.get("secondarySegments", [])],
                "principaisProdutosAtendimento": [opt.get("value") for opt in
                                                  profile.get("additionalFields", [{}])[0].get("options",
                                                                                               [])] if profile.get(
                    "additionalFields") else []
            }
            dossie.operacional = OperacionalDTO.model_validate(operacional_data)

            company_flags = profile.get("companyPageFlags") or {}
            engajamento_data = {
                "statusConta": profile.get("status"),
                "verificada": company_flags.get("hasVerificada"),
                "tipoPlano": company_flags.get("configurationType")
            }
            dossie.engajamento_plataforma = EngajamentoDTO.model_validate(engajamento_data)

            reputacao_map = {}
            for panel in profile.get("panels", []):
                index = panel.get("index", {})
                tipo = index.get("type")
                if tipo:
                    reputacao_map[tipo] = ReputacaoPeriodoDTO.model_validate(index)
            dossie.reputacao_por_periodo = reputacao_map
        else:
            # --- Lógica de fallback para empresas não verificadas ---
            ident_data = {
                "idReclameAqui": initial_data.id,
                "razaoSocial": initial_data.company_name,
                "nomeFantasia": initial_data.fantasy_name,
                "cnpj": initial_data.documents[0] if initial_data.documents else None
            }
            identificacao = IdentificacaoDTO.model_validate(ident_data)
            dossie = DossieEmpresaDTO(identificacao=identificacao)

            if evolution:
                reputacao_map = {}
                snapshot = evolution.get("snapshots", [{}])[0]
                if snapshot:
                    reputacao_map["SIX_MONTHS"] = self._calculate_reputation_from_snapshot(snapshot)
                dossie.reputacao_por_periodo = reputacao_map

        # --- Preenchimento dos dados comuns, que vêm de outras APIs ---
        if main_problems:
            problemas = main_problems.get("complainResult", {}).get("complains", {}).get("problems", [])
            dossie.principais_problemas_historico = [ProblemInfoDTO.model_validate(p) for p in problemas[:5]]

        if problems_6_months:
            problemas = problems_6_months.get("complainResult", {}).get("complains", {}).get("problems", [])
            dossie.principais_problemas_6_meses = [ProblemInfoDTO.model_validate(p) for p in problemas]

        if evolution:
            dossie.evolucao_mensal_detalhada = evolution.get("snapshots")

        return dossie

    def _calculate_reputation_from_snapshot(self, snapshot: Dict) -> ReputacaoPeriodoDTO:
        """Método auxiliar para calcular a reputação a partir de um snapshot do indexEvolution."""
        total_reclamacoes = snapshot.get("totalIndexable", 0)
        total_resolvidas = snapshot.get("totalSolved", 0)
        total_avaliacoes = snapshot.get("totalEvaluations", 0)
        total_voltaria = snapshot.get("totalDealAgain", 0)

        perc_resolucao = (total_resolvidas / total_reclamacoes * 100) if total_reclamacoes > 0 else 0
        perc_satisfacao = (total_voltaria / total_avaliacoes * 100) if total_avaliacoes > 0 else 0

        return ReputacaoPeriodoDTO(
            type="SIX_MONTHS",
            status=snapshot.get("status", "N/A"),
            finalScore=0.0,  # Este dado não está disponível nesta API
            totalComplains=total_reclamacoes,
            solvedPercentual=round(perc_resolucao, 1),
            dealAgainPercentual=round(perc_satisfacao, 1)
        )