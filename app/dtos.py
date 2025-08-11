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
Define todos os modelos de dados (DTOs - Data Transfer Objects) da aplicação.
Estas classes, baseadas no Pydantic, garantem a validação, serialização e
deserialização dos dados entre as APIs externas e a nossa aplicação.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any


# --- DTOs para a busca inicial ---

class CompanyDTO(BaseModel):
    """Representa os dados básicos de uma empresa retornados pela busca inicial."""
    id: str
    company_name: str = Field(..., alias='companyName')
    fantasy_name: str = Field(..., alias='fantasyName')
    shortname: str
    status: str
    documents: List[str]


class SearchResponseDTO(BaseModel):
    """Representa a resposta completa da API de busca inicial."""
    companies: List[CompanyDTO]


# --- DTOs para o Dossiê 360° Final ---

class ProblemInfoDTO(BaseModel):
    """Representa a informação sobre um tipo de problema e a sua frequência."""
    nome: str = Field(..., alias='name')
    quantidade: int = Field(..., alias='count')
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class ReputacaoPeriodoDTO(BaseModel):
    """Representa o painel de reputação para um determinado período (ex: 6 meses)."""
    periodo: str = Field(..., alias='type')
    reputacao: str = Field(..., alias='status')
    nota_final: Any = Field(..., alias='finalScore')
    total_reclamacoes: int = Field(..., alias='totalComplains')
    percentual_resolucao: Any = Field(..., alias='solvedPercentual')
    percentual_voltaria_fazer_negocio: Any = Field(..., alias='dealAgainPercentual')
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class EnderecoDTO(BaseModel):
    """Representa o endereço de uma empresa."""
    cep: Optional[str] = Field(None, alias='zipCode')
    logradouro: Optional[str] = Field(None, alias='route')
    bairro: Optional[str] = Field(None, alias='neighborhood')
    cidade: Optional[str] = Field(None, alias='city')
    estado: Optional[str] = Field(None, alias='state')
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class IdentificacaoDTO(BaseModel):
    """Representa os dados cadastrais e de identificação de uma empresa."""
    id_reclame_aqui: str = Field(..., alias='idReclameAqui')
    cnpj: Optional[str] = None
    razao_social: str = Field(..., alias='razaoSocial')
    nome_fantasia: str = Field(..., alias='nomeFantasia')
    data_cadastro_plataforma: Optional[str] = Field(None, alias='dataCadastroPlataforma')
    endereco: Optional[EnderecoDTO] = None
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class OperacionalDTO(BaseModel):
    """Representa os dados operacionais de uma empresa (segmentos, site, etc.)."""
    segmento_principal: Optional[str] = Field(None, alias='segmentoPrincipal')
    segmentos_secundarios: List[str] = Field([], alias='segmentosSecundarios')
    site_principal: Optional[str] = Field(None, alias='sitePrincipal')
    principais_produtos_atendimento: List[str] = Field([], alias='principaisProdutosAtendimento')
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class EngajamentoDTO(BaseModel):
    """Representa o nível de engajamento da empresa com a plataforma ExposeAqui Aqui."""
    status_conta: Optional[str] = Field(None, alias='statusConta')
    verificada: Optional[bool] = None
    tipo_plano: Optional[str] = Field(None, alias='tipoPlano')
    model_config = ConfigDict(populate_by_name=True, by_alias=True)


class DossieEmpresaDTO(BaseModel):
    """O DTO final e completo, que representa o Panorama 360° da empresa."""
    identificacao: IdentificacaoDTO
    operacional: Optional[OperacionalDTO] = None
    engajamento_plataforma: Optional[EngajamentoDTO] = Field(None, alias='engajamentoPlataforma')
    reputacao_por_periodo: Optional[Dict[str, ReputacaoPeriodoDTO]] = Field(None, alias='reputacaoPorPeriodo')
    principais_problemas_historico: Optional[List[ProblemInfoDTO]] = Field(None, alias='principaisProblemasHistorico')
    principais_problemas_6_meses: Optional[List[ProblemInfoDTO]] = Field(None, alias='principaisProblemas6Meses')
    evolucao_mensal_detalhada: Optional[Any] = Field(None, alias='evolucaoMensalDetalhada')

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True  # Garante que o JSON de saída use os aliases em camelCase
    )