# Arquitetura Multi-Tenant com Docker e Traefik

Este documento descreve a arquitetura e o fluxo de trabalho para manter múltiplas instâncias da aplicação web CMS rodando o mesmo código fonte, mas com dados, bancos e domínios totalmente independentes.

## 1. Princípios Básicos

A aplicação foi projetada para ser parametrizável. Isso significa que configurações sensíveis ou que mudam entre diferentes "sites" são lidas a partir de variáveis de ambiente, não estando "chumbadas" no código fonte. 

A variável mais importante neste contexto é o caminho do banco de dados (por exemplo, `DATABASE_URL=sqlite:////app/data/site_cms.db`), permitindo que a mesma aplicação aponte para arquivos diferentes dependendo da instância em que está rodando.

## 2. Docker e Isolamento de Dados

A base da implantação é a criação de uma única **Imagem Docker** que engloba tanto o Front-end (React/Vite) quanto o Back-end (Python/FastAPI).

### Regra de Ouro:
**Os dados (arquivos do SQLite, imagens de upload, etc.) não podem ficar dentro da imagem do Docker.**
Eles devem ser persistidos no servidor (na máquina hospedeira) através do uso de **Volumes** do Docker. Isso permite que você atualize o código da aplicação (destruindo e recriando o contêiner) sem perder os dados de nenhum dos sites.

## 3. Ambiente de Desenvolvimento (Múltiplas Portas)

Para desenvolvimento local, utilizamos o `docker-compose.yml`. Podemos subir dois ou mais sites simultaneamente mapeando volumes diferentes para a mesma imagem, e expondo-os em portas distintas.

**Exemplo de `docker-compose.yml` para desenvolvimento:**

```yaml
version: '3.8'

services:
  # Instância 1 (Ex: Site de Mestrado)
  site-mestrado:
    image: meu-cms-app:latest
    ports:
      - "8001:8000" # Acesso local via http://localhost:8001
    volumes:
      - ./dados/mestrado:/app/data
    environment:
      - DATABASE_URL=sqlite:////app/data/site_cms.db

  # Instância 2 (Ex: Site de Doutorado)
  site-doutorado:
    image: meu-cms-app:latest
    ports:
      - "8002:8000" # Acesso local via http://localhost:8002
    volumes:
      - ./dados/doutorado:/app/data
    environment:
      - DATABASE_URL=sqlite:////app/data/site_cms.db
```

Com o comando `docker compose up -d`, ambas as instâncias iniciam. O sistema verificará se o banco existe em suas respectivas pastas (`./dados/mestrado` e `./dados/doutorado`). Se não existir, criará bancos de dados em branco separados.

## 4. Ambiente de Produção (Subdomínios via Proxy Reverso)

Em um ambiente de produção (um servidor VPS), não é elegante expor portas (como `:8001` ou `:8002`) para o usuário final. Em vez disso, utilizamos **Subdomínios** (ex: `mestrado.meusite.com` e `doutorado.meusite.com`).

Para isso, usamos um **Proxy Reverso**. A ferramenta recomendada para ambientes Docker é o **Traefik**, devido à sua integração nativa (auto-discovery) e facilidade na geração de certificados SSL gratuitos via Let's Encrypt.

### Como funciona com Traefik:
Em vez de mapear portas diretamente (`ports:`), nós usamos etiquetas (`labels:`) para dizer ao Traefik por qual subdomínio aquele contêiner é responsável. O Traefik fica exposto na porta 80 e 443 do servidor, recebe todas as requisições web, e as roteia internamente para o contêiner correto.

**Exemplo de `docker-compose.yml` para produção:**

```yaml
version: '3.8'

services:
  # O Proxy Reverso que roteia o tráfego
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      # Configurações de certificados Let's Encrypt iriam aqui...
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  # Instância 1 (Subdomínio A)
  site-mestrado:
    image: meu-cms-app:latest
    volumes:
      - /var/www/dados/mestrado:/app/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.site-mestrado.rule=Host(`mestrado.meusite.com`)"
      - "traefik.http.routers.site-mestrado.entrypoints=websecure"
      - "traefik.http.routers.site-mestrado.tls.certresolver=myresolver"

  # Instância 2 (Subdomínio B)
  site-doutorado:
    image: meu-cms-app:latest
    volumes:
      - /var/www/dados/doutorado:/app/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.site-doutorado.rule=Host(`doutorado.meusite.com`)"
      - "traefik.http.routers.site-doutorado.entrypoints=websecure"
      - "traefik.http.routers.site-doutorado.tls.certresolver=myresolver"
```

## 5. Fluxo de Criação de um Novo Site

Com essa arquitetura, criar um novo site baseado na aplicação é um processo que leva segundos e **não envolve mexer no código**:

1. Crie uma nova pasta vazia no servidor (ex: `/var/www/dados/novo-projeto`).
2. Adicione um novo bloco (serviço) ao `docker-compose.yml` da produção.
3. Configure as `labels` apontando para o novo subdomínio (ex: `novo.meusite.com`).
4. Rode `docker compose up -d` para atualizar os serviços.
5. O Traefik detecta o novo contêiner automaticamente e já começa a rotear o tráfego e provisionar o certificado SSL. A aplicação boota, cria o SQLite em branco na nova pasta, e o novo site já está no ar aguardando ser alimentado pelo painel administrativo.
