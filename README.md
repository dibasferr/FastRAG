# FastRAG - Minimal Retrieval-Augmented Generation API

Um projeto simples que demonstra como construir um sistema **Retrieval-Augmented Generation (RAG)** utilizando **FastAPI**, **Sentence Transformers** e a **API da Groq**.

O objetivo é mostrar, de forma minimalista, como um modelo de linguagem pode responder perguntas recorrendo apenas ao documento mais relevante recuperado através de pesquisa semântica.

---

# Índice

- [Visão Geral](#-visão-geral)
- [Como Funciona](#-como-funciona)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Execução](#-execução)
- [Exemplo de Utilização](#-exemplo-de-utilização)
- [Limitações](#-limitações)

---

# Visão Geral

Este projeto implementa uma pipeline simplificada de **Retrieval-Augmented Generation (RAG)**.

Em vez de permitir que um LLM responda utilizando apenas o seu conhecimento interno, o sistema:

1. recebe uma pergunta do utilizador;
2. converte a pergunta em um **embedding**;
3. compara esse embedding com os embeddings dos documentos armazenados;
4. identifica o documento semanticamente mais semelhante;
5. envia apenas esse documento para o modelo de linguagem;
6. devolve uma resposta baseada exclusivamente nesse contexto.

---

# Como Funciona

```text
                Pergunta
                    │
                    ▼
          Sentence Transformer
                    │
          Embedding da Pergunta
                    │
                    ▼
        Similaridade de Cosseno
                    │
                    ▼
      Documento Mais Relevante
                    │
                    ▼
      Prompt com Contexto
                    │
                    ▼
        Groq API (Llama 3.1)
                    │
                    ▼
              Resposta Final
```

---

# Pesquisa Semântica

Os documentos são indexados através do modelo:

```
all-MiniLM-L6-v2
```

Sempre que uma consulta é recebida:

- é criado um embedding da pergunta;
- calcula-se a similaridade de cosseno entre a pergunta e todos os documentos;
- seleciona-se o documento com maior similaridade.

---

# Geração da Resposta

Após recuperar o documento mais relevante, é criado um prompt semelhante a:

```text
You are an AI assistant.

Answer based ONLY on this document:

<documento>

User:
<pergunta>

Assistant:
```

Este prompt é enviado para a API da **Groq**, utilizando o modelo:

```
llama-3.1-8b-instant
```

---

# Tecnologias Utilizadas

- Python
- FastAPI
- Sentence Transformers
- PyTorch
- Pydantic
- Requests
- Uvicorn
- Groq API
- Llama 3.1

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USERNAME/FastRAG.git
```

Entre na pasta:

```bash
cd FastRAG
```

Instale as dependências:

```bash
pip install fastapi uvicorn sentence-transformers requests pydantic
```

---

# Configuração

É necessário possuir uma chave da **Groq API**.

Defina a variável de ambiente:

### Linux / macOS

```bash
export GROQ_API_KEY="SUA_API_KEY"
```

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="SUA_API_KEY"
```

---

# Execução

Execute:

```bash
python fastrag.py
```

ou

```bash
uvicorn fastrag:app --reload
```

A API ficará disponível em:

```
http://localhost:8000
```

Documentação automática:

```
http://localhost:8000/docs
```

---

# Endpoint

## POST `/query`

### Request

```json
{
    "query": "Who invented Facebook?"
}
```

### Response

```json
{
    "response": "According to the retrieved document, Facebook was invented by Pedro Bras Ferreira..."
}
```

---

# Base de Conhecimento

Neste exemplo, a base de conhecimento é composta por uma pequena lista de documentos armazenados em memória.

```python
documents = [
    {...},
    {...},
    ...
]
```

Num sistema real, estes documentos poderiam ser carregados de:

- PDFs
- Bases de dados
- Elasticsearch
- ChromaDB
- Pinecone
- Weaviate
- FAISS

---

# Objetivos do Projeto

Este projeto pretende demonstrar os conceitos fundamentais de um sistema RAG:

- geração de embeddings;
- pesquisa semântica;
- recuperação de contexto;
- construção de prompts;
- integração com um Large Language Model;
- criação de uma API REST com FastAPI.

---

# Limitações

Por simplicidade, esta implementação possui algumas limitações:

- os documentos são armazenados em memória;
- apenas o documento mais semelhante é utilizado;
- não existe armazenamento vetorial (Vector Database);
- não existe re-ranking;
- não existe chunking de documentos;
- não existe memória conversacional.

Apesar disso, o projeto ilustra claramente o funcionamento essencial de uma arquitetura **Retrieval-Augmented Generation (RAG)**.

---

# Melhorias Futuras

Possíveis evoluções incluem:

- utilização de FAISS ou ChromaDB;
- recuperação dos Top-K documentos;
- re-ranking com Cross Encoder;
- suporte para PDFs;
- chunking automático;
- streaming de respostas;
- histórico de conversação;
- Docker;
- testes automatizados.

---

# Conceitos Demonstrados

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Sentence Embeddings
- Cosine Similarity
- Prompt Engineering
- FastAPI
- REST APIs
- Large Language Models (LLMs)
