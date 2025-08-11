# 🚀 ExposedAqui: Um Dossiê 360° sobre Empresas 🕵️‍♀️✨

**Versão:** 2.0.0 (Tiro de Canhão)
<br>
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-orange.svg)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

---

### Visão Geral

**ExposedAqui** é uma API de alta performance para a coleta e análise de dados de reputação de empresas a partir do site Reclame Aqui. O projeto nasceu da necessidade de obter dados públicos de forma estruturada e escalável, contornando a ausência de uma API pública.

O que começou como um scraper tradicional evoluiu para uma solução sofisticada que não utiliza navegadores. Em vez disso, ela comunica-se diretamente com as APIs do site através da simulação do comportamento de um cliente legítimo, uma abordagem que nos permitiu contornar as robustas medidas de segurança do Cloudflare e alcançar uma performance milhares de vezes superior à automação de navegador.

## 📖 A História Completa (Leia na nossa Wiki!)

A jornada para criar o **ExposedAqui** foi uma saga fascinante de engenharia reversa, depuração e descobertas. Desde os becos sem saída com o Playwright até à epifania da "entrevista de emprego" que nos permitiu enganar o Cloudflare, documentámos tudo.

### **➡️ [Clique aqui para ler a história completa e todos os detalhes técnicos na Wiki do projeto!](https://github.com/madmilena/ExposeAqui/wiki)**

---

### 🚀 Como Usar o Projeto

#### Pré-requisitos
* Python 3.11+
* Docker

#### Configuração Local
1.  Clone o repositório.
2.  Crie e ative um ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

#### Executando Localmente
1.  Para iniciar o servidor:
    ```bash
    python3 app/main.py
    ```
2.  A API estará no ar em `http://127.0.0.1:8000`.
3.  Acesse a documentação interativa (Swagger UI) em `http://127.0.0.1:8000/docs` para testar.

#### Executando com Docker
1.  Construa a imagem Docker:
    ```bash
    docker build -t exposeaqui-api .
    ```
2.  Execute o container:
    ```bash
    docker run -p 8000:8000 --rm exposeaqui-api
    ```

---

### **AVISO LEGAL E DIREITOS AUTORAIS**

* **Copyright (C) 2025 Milena Madsen. Todos os direitos reservados.**
* **Autora:** Milena Madsen
* **Contacto:** milena.madsen@aol.com
* **GitHub:** https://github.com/madmilena

Este software foi desenvolvido para fins de estudo e pesquisa. O uso indevido deste software para violar os Termos de Serviço de qualquer site é estritamente proibido. A autora não se responsabiliza por qualquer uso indevido deste código.
