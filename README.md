# 🚀 ExposedAqui: Um Dossiê 360° sobre Empresas 🕵️‍♀️✨

**Versão:** 2.0.0 (Tiro de Canhão)
<br>
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-orange.svg)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.35.0-blue)
![curl_cffi](https://img.shields.io/badge/curl_cffi-0.13.0-brightgreen)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

---

### **AVISO LEGAL E DIREITOS AUTORAIS**

* **Copyright (C) 2025 Milena Madsen. Todos os direitos reservados.**
* **Autora:** Milena Madsen
* **Contato:** milena.madsen@aol.com
* **GitHub:** https://github.com/madmilena

Este software foi desenvolvido para fins de estudo, pesquisa e prova de conceito. O seu objetivo é demonstrar técnicas avançadas de coleta, análise de dados e design de software.

O uso indevido deste software para violar os Termos de Serviço de qualquer site, incluindo, mas não se limitando a `reclameaqui.com.br` e `cloudflare.com`, é estritamente proibido. A autora não se responsabiliza por qualquer uso indevido deste código ou por quaisquer consequências legais, financeiras ou de qualquer outra natureza decorrentes de tal uso. Use por sua conta e risco.

---

### 🚀 Como Usar o Projeto

Para quem quer ir direto ao ponto e ver a mágica acontecer.

#### Pré-requisitos
* Python 3.11+
* Docker (para a execução em container)

#### Configuração Local
1.  Clone o repositório.
2.  Crie e ative um ambiente virtual (boa prática!):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

#### Executando Localmente
1.  Para iniciar o servidor em modo de desenvolvimento (com recarregamento automático):
    ```bash
    python3 app/main.py
    ```

2.  A API estará no ar em `http://127.0.0.1:8000`.
3.  A documentação interativa (Swagger) que o FastAPI gera para nós estará em `http://127.0.0.1:8000/docs`.

#### Executando com Docker
1.  Construa a imagem Docker:
    ```bash
    docker build -t exposeaqui-api .
    ```
2.  Execute o container. Para customizar a porta, altere o primeiro número (ex: `-p 5000:8000`):
    ```bash
    docker run -p 8000:8000 --rm exposeaqui-api
    ```
A API estará disponível em `http://localhost:8000`.

### 💻 Tecnologias Utilizadas

* **FastAPI:** Framework web moderno e de alta performance para construir nossa API. Rápido como um foguete! 🚀
* **Pydantic:** Para validação de dados robusta e serialização de JSON, garantindo que nossos "dossiês" estejam sempre corretos e bem estruturados.
* **curl_cffi:** Nossa "arma secreta". Uma biblioteca Python que nos permite fazer requisições HTTP imitando perfeitamente um navegador a nível de rede, sendo a chave para o nosso sucesso.
* **Docker:** Para empacotar nossa aplicação num ambiente portátil e escalável, pronta para a produção.

### 🏛️ Arquitetura e Design Patterns

Para garantir que o código não virasse um "monstrinho", aplicamos as melhores práticas de engenharia de software, inspiradas nos princípios **SOLID**.

* **Princípio da Responsabilidade Única (SRP):** Quebramos a aplicação em componentes especializados, como numa cozinha profissional:
    * `ReclameAquiScraper`: É o "Comprador". Sua única responsabilidade é ir ao "mercado" (o site) e coletar os dados brutos, sem se importar com a receita.
    * `DossieGenerator`: É o "Chef". Sua única responsabilidade é pegar os ingredientes crus e transformá-los no "prato final" (o dossiê), aplicando nossa lógica de negócio.
    * `SearchService`: É o "Gerente". Ele orquestra o trabalho, chamando o Comprador e depois o Chef.

* **Strategy Pattern:** Usamos interfaces (`ScraperStrategy`, `AnalysisStrategy`) para que, no futuro, possamos facilmente adicionar novos "Compradores" (para buscar dados do Serasa, por exemplo) sem alterar o código que já funciona.

---

## 📖 A Nossa Saga: A História por Trás do Código

O que começou como um simples projeto de scraping evoluiu para uma fascinante jornada de engenharia reversa. O código que você vê aqui não foi nossa primeira tentativa, mas sim o culminar de muitas batalhas e descobertas. Eu (Milena) e minhas IAs de confiança (Gemini Pro, ChatGPT e DeepSeek) passamos por poucas e boas para chegar aqui, e esta é nossa história.

### O Sonho: Um Raio-X da Reputação das Empresas 🎯

A ideia era simples, mas poderosa: criar uma API que pudesse fornecer um dossiê completo sobre a reputação de qualquer empresa no Reclame Aqui. Um verdadeiro Raio-X 360°, útil para tudo, desde uma simples consulta até alimentar um sistema de birô de crédito. Mas como obter os dados, se eles são vendidos a peso de ouro em APIs privadas?

### O Pesadelo Inicial: O Monstrinho da Tasmânia em Java 🐌

Nossa primeira versão foi um scraper em Java com **Playwright**. Parecia a escolha óbvia: simular um navegador real. Funcionou, mas era um monstro. Uma única consulta demorava em média **16 longos segundos**. Era pesado, consumia uma quantidade absurda de recursos e, pior de tudo, era frágil. Após algumas buscas, o site nos "sacava" e bloqueava. Para uma aplicação que sonhava com escala, era um beco sem saída.

### O Mapa do Tesouro: As APIs do Reclame Aqui 🗺️

Antes de desistir, usamos o Playwright para uma última missão: espionagem. Com as **Ferramentas de Desenvolvedor (F12)** do navegador abertas, agimos como detetives. Mapeamos cada chamada de rede que o site fazia. Descobrimos que ele usa uma arquitetura brilhante, com APIs específicas para cada pedaço de informação. Encontramos os "endereços" de tudo: a busca, os problemas históricos, a evolução mensal e, a "jóia da coroa", uma API de perfil completo para empresas verificadas. Tínhamos o mapa do tesouro. O problema é que o tesouro era guardado por um dragão.

### A Epifania: A Entrevista de Emprego 🕵️‍♀️

Ao tentarmos chamar as APIs que descobrimos com um código simples, batemos numa muralha: `Erro 403 Forbidden`. No início, a frustração foi imensa. Foi ao inspecionar a resposta que vimos a palavra mágica: `server: cloudflare`. Não estávamos lutando contra o site, mas contra um dos sistemas de segurança mais avançados do mundo.

Foi aí que a virada de chave aconteceu, com uma metáfora que guiou toda a nossa pesquisa:

> *"Sabia que empresas contratam algumas pessoas sem qualificação profissional, acreditando que a pessoa contratada seria a pessoa qualificada?"* — questionei o Gemini, que ficou sem entender a relação com o problema, mas logo continuei:
>
> *"Os recrutadores nem sempre sabem quem é a melhor pessoa para um cargo, mas são treinados para reconhecer perfis. Um candidato qualificado passa porque tem as 'skills'. Ja as pessoas desqualificadas que conseguem os empregos falando bonito e dizendo tudo o que o recrutador espera ouvir do candidato.* - Gemini entendeu de primeira a metáfora e logo devolveu:
> 
> *"Os candidatos não esdudaram as qualificações. Elas estudaram o recrutador! E se fizéssemos o mesmo com o Cloudflare?"*

Esta epifania mudou tudo. Deixamos de pensar como programadores tentando "forçar a entrada" e passamos a pensar como investigadores tentando **"passar na entrevista"**.

Estudamos um "candidato qualificado" (um navegador real) e descobrimos seus segredos. O Cloudflare não olhava só nosso "currículo" (`User-Agent`). Ele analisava nosso "aperto de mão" (a assinatura TLS/JA3 da conexão), nossa "vestimenta" (a consistência de dezenas de cabeçalhos) e, finalmente, aplicava uma "prova" (o desafio JavaScript).

Armados com este conhecimento, construímos nosso "candidato perfeito" em Python. Um sósia que sabia dar o aperto de mão certo, vestir-se de forma impecável e responder à prova de forma convincente. O resultado? Uma consulta que demorava **16 segundos**, agora é executada em **menos de 2 segundos**. Um salto quântico não só em performance, mas em inteligência.

### 10. Créditos e Agradecimentos ❤️

Este projeto foi uma jornada de descoberta, engenharia e perseverança.

* **Autora e Investigadora Principal:** Milena Madsen
* **Assistentes de Pesquisa e Desenvolvimento de IA:**
    * **Gemini Pro (Google):** Pela sua capacidade de análise profunda, refatoração de código e por me ajudar a documentar esta saga.
    * **ChatGPT (OpenAI) & DeepSeek:** Pelas suas contribuições na desofuscação inicial do código e por oferecerem perspetivas alternativas durante nossa investigação.