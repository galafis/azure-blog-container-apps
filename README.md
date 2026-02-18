# Blog com Azure Container Apps

## Desafio de Projeto - DIO Microsoft Azure Cloud Native 2026

### Descrição

Projeto desenvolvido como parte do bootcamp Microsoft Azure Cloud Native 2026 da DIO. O objetivo é demonstrar a criação de um blog utilizando Azure Container Apps, aplicando conceitos de containerização, orquestração e deploy na nuvem.

### Tecnologias Utilizadas

- **Azure Container Apps** - Plataforma serverless para execução de contêineres
- **Azure Container Registry (ACR)** - Registro privado de imagens Docker
- **Docker** - Containerização da aplicação
- **Azure CLI** - Gerenciamento de recursos via linha de comando

### Arquitetura

```
[Dockerfile] -> [ACR Build] -> [Container Registry] -> [Container Apps Environment] -> [Blog App]
```

### Passos Realizados

1. **Criação do Dockerfile** - Configuração do ambiente containerizado
2. **Resource Group e ACR** - Provisionamento da infraestrutura base
3. **Build e Push da Imagem** - Upload para o Azure Container Registry
4. **Deploy no Container Apps** - Publicação com escalabilidade automática
5. **Configuração de Ingress** - Exposição pública via HTTPS

### Principais Aprendizados

- Container Apps abstrai a complexidade do Kubernetes
- ACR integra nativamente com Container Apps
- Escalabilidade automática baseada em demanda (scale-to-zero)
- Revisões permitem deploy blue/green e canary
- Segredos gerenciados de forma segura no ambiente

### Comandos Principais

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

### Estrutura do Projeto

```
/
|-- Dockerfile
|-- README.md
|-- src/
|   |-- index.html
|   |-- styles.css
```

---

**Autor:** Gabriel Demetrios Lafis  
**Bootcamp:** Microsoft Azure Cloud Native 2026 - DIO
