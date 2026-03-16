# Blog Platform with Azure Container Apps / Plataforma de Blog com Azure Container Apps

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Microsoft_Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License-MIT](https://img.shields.io/badge/License--MIT-yellow?style=for-the-badge)

</div>


## English

### About the Project

A blog platform with a Flask-like API architecture, built for deployment on Azure Container Apps. Features a complete content management system with posts, categories, tags, comments, and a built-in markdown-to-HTML renderer. Uses in-memory storage to simulate database operations with full CRUD support.

### Architecture

```
azure-blog-container-apps/
|-- app/
|   |-- models.py                  # Post, Category, Tag, Comment dataclasses
|   |-- database.py                # In-memory DB with CRUD operations
|   |-- routes/
|   |   |-- posts.py               # Post API endpoint handlers
|   |   |-- comments.py            # Comment API endpoint handlers
|   |-- services/
|   |   |-- markdown_renderer.py   # Markdown to HTML converter
|-- tests/
|   |-- test_blog.py               # 20+ unit tests
|-- main.py                        # Demo script
|-- requirements.txt
|-- .gitignore
|-- README.md
```

### Key Features

- **Post Management**: Full CRUD with publish/unpublish workflow
- **Categories & Tags**: Organize content with categories and tags
- **Comment System**: Threaded comments with moderation (approve/reject)
- **Markdown Rendering**: Built-in converter supporting headers, bold, italic, code blocks, links, lists, blockquotes
- **Slug Generation**: Automatic URL-friendly slug creation from titles
- **Filtering**: Query posts by author, category, tag, or publish status
- **Statistics**: Dashboard stats for posts, comments, and moderation queue

### How to Run

```bash
# Clone the repository
git clone https://github.com/galafis/azure-blog-container-apps.git
cd azure-blog-container-apps

# Install dependencies
pip install -r requirements.txt

# Run the demo
python main.py

# Run tests
pytest tests/ -v
```

### Technologies

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| pytest | Testing framework |
| dataclasses | Data models |

---

## Portugues

### Sobre o Projeto

Plataforma de blog com arquitetura de API estilo Flask, construida para deploy no Azure Container Apps. Possui um sistema completo de gerenciamento de conteudo com posts, categorias, tags, comentarios e um renderizador de markdown para HTML integrado. Utiliza armazenamento em memoria para simular operacoes de banco de dados com suporte completo a CRUD.

### Funcionalidades Principais

- **Gerenciamento de Posts**: CRUD completo com fluxo de publicar/despublicar
- **Categorias e Tags**: Organize conteudo com categorias e tags
- **Sistema de Comentarios**: Comentarios com respostas encadeadas e moderacao
- **Renderizacao Markdown**: Conversor integrado com suporte a cabecalhos, negrito, italico, blocos de codigo, links, listas e citacoes
- **Geracao de Slug**: Criacao automatica de slugs amigaveis para URL
- **Filtragem**: Consulte posts por autor, categoria, tag ou status de publicacao
- **Estatisticas**: Painel com estatisticas de posts, comentarios e fila de moderacao

### Como Executar

```bash
# Clonar o repositorio
git clone https://github.com/galafis/azure-blog-container-apps.git
cd azure-blog-container-apps

# Instalar dependencias
pip install -r requirements.txt

# Executar o demo
python main.py

# Executar os testes
pytest tests/ -v
```

### Deploy no Azure Container Apps

```bash
# Criar Resource Group
az group create --name rg-blog --location eastus

# Criar Container Registry
az acr create --name acrblogapp --resource-group rg-blog --sku Basic

# Build da imagem no ACR
az acr build --registry acrblogapp --image blog-app:v1 .

# Criar Container App
az containerapp create \
  --name blog-container-app \
  --resource-group rg-blog \
  --environment blog-env \
  --image acrblogapp.azurecr.io/blog-app:v1 \
  --target-port 80 \
  --ingress external
```

### Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.10+ | Linguagem principal |
| pytest | Framework de testes |
| dataclasses | Modelos de dados |
| Azure Container Apps | Plataforma de deploy |

## Autor / Author

**Gabriel Demetrios Lafis**
