"""
API-ponte do Fórum de Discussões -- serviço compartilhado, implantado uma única vez no
Render, para atender VÁRIAS landing pages estáticas (esta dissertação, a da esposa, a de
colegas etc.), sem exigir que cada pessoa crie conta própria no Render.

Cada site é 100% estático no GitHub Pages: sem banco de dados, sem servidor próprio em
produção. Para permitir que visitantes publiquem perguntas/respostas sem precisar de conta
(GitHub, Google etc.), este serviço recebe o POST e grava a pergunta/resposta diretamente
no JSON do repositório correspondente via API do GitHub (Contents API) -- ou seja, o
próprio repositório git de cada projeto funciona como "banco de dados" gratuito e
permanente. Esse commit dispara o workflow de deploy já existente em cada repo
(.github/workflows/deploy.yml), então a pergunta aparece no site ao vivo depois do próximo
build (alguns minutos).

Para adicionar um novo projeto (nova landing page):
  1. Acrescentar uma entrada em PROJETOS abaixo (repo + tópicos válidos daquele site).
  2. Garantir que o token em GITHUB_TOKEN tenha acesso de escrita (Contents: Read and
     write) também ao repositório desse novo projeto -- um fine-grained PAT pode ser
     escopado a vários repositórios ao mesmo tempo.
  3. Acrescentar o domínio do GitHub Pages desse site à env var ALLOWED_ORIGINS no Render.
  4. git push -- o Render reimplanta automaticamente.

Sem moderação automática: qualquer um pode postar direto, sem revisão prévia. Para reduzir
abuso há apenas: honeypot, limite de tamanho de texto e um rate-limit simples por IP (em
memória -- reseta quando o serviço reinicia/dorme, é só uma camada leve, não é à prova de
bots sofisticados).
"""
import base64
import json
import os
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]  # fine-grained PAT com Contents:read/write nos repos de PROJETOS
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")
DATA_PATH_IN_REPO = "web_app/frontend/src/data/forum_perguntas.json"

GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ALLOWED_ORIGINS", "https://ocimarlz.github.io,http://localhost:5173"
    ).split(",")
    if o.strip()
]


@dataclass(frozen=True)
class Projeto:
    repo: str  # "dono/repositorio" no GitHub
    topicos: frozenset[str]  # slugs válidos, sincronizados com forumTopicos.ts daquele site


# Um projeto por landing page que usa este serviço compartilhado.
PROJETOS: dict[str, Projeto] = {
    "ocimar-mestrado-ppge": Projeto(
        repo="OcimarLZ/mestrado-ppge",
        topicos=frozenset(
            {
                "ead-e-qualidade-da-formacao",
                "publico-x-privado-na-educacao-superior",
                "duvidas-sobre-a-pesquisa",
            }
        ),
    ),
    # "nome-do-proximo-projeto": Projeto(repo="dono/outro-repo", topicos=frozenset({...})),
}

RATE_LIMIT_WINDOW_SECONDS = 600
RATE_LIMIT_MAX_SUBMISSOES = 5
_submissoes_por_ip: dict[str, list[float]] = defaultdict(list)


def checar_rate_limit(ip: str) -> None:
    agora = time.time()
    historico = _submissoes_por_ip[ip]
    historico[:] = [t for t in historico if agora - t < RATE_LIMIT_WINDOW_SECONDS]
    if len(historico) >= RATE_LIMIT_MAX_SUBMISSOES:
        raise HTTPException(429, "Muitas submissões recentes, tente novamente mais tarde.")
    historico.append(agora)


def sanitizar(texto: str | None, tamanho_max: int) -> str:
    if not texto:
        return ""
    return texto.strip()[:tamanho_max]


def resolver_projeto(projeto_slug: str, topico: str) -> Projeto:
    projeto = PROJETOS.get(projeto_slug)
    if not projeto:
        raise HTTPException(400, "Projeto inválido.")
    if topico not in projeto.topicos:
        raise HTTPException(400, "Tópico inválido.")
    return projeto


class NovaPergunta(BaseModel):
    projeto: str
    topico: str
    pergunta: str
    nome: str | None = None
    site: str = Field(default="", description="honeypot -- deve ficar vazio")


class NovaResposta(BaseModel):
    projeto: str
    topico: str
    pergunta_id: str
    resposta: str
    nome: str | None = None
    site: str = Field(default="", description="honeypot -- deve ficar vazio")


def url_arquivo(projeto: Projeto) -> str:
    return f"https://api.github.com/repos/{projeto.repo}/contents/{DATA_PATH_IN_REPO}"


async def buscar_arquivo(projeto: Projeto) -> tuple[dict, str]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            url_arquivo(projeto), headers=GITHUB_HEADERS, params={"ref": GITHUB_BRANCH}
        )
    if r.status_code != 200:
        raise HTTPException(502, "Não foi possível ler os dados do fórum no GitHub.")
    payload = r.json()
    conteudo = base64.b64decode(payload["content"]).decode("utf-8")
    return json.loads(conteudo), payload["sha"]


async def publicar_arquivo(projeto: Projeto, dados: dict, sha: str, mensagem: str) -> httpx.Response:
    bruto = json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8")
    body = {
        "message": mensagem,
        "content": base64.b64encode(bruto).decode("ascii"),
        "sha": sha,
        "branch": GITHUB_BRANCH,
    }
    async with httpx.AsyncClient() as client:
        return await client.put(url_arquivo(projeto), headers=GITHUB_HEADERS, json=body)


async def commitar_mudanca(projeto: Projeto, mutar: "callable", mensagem: str) -> None:
    """Lê o JSON atual, aplica `mutar`, e grava de volta. Tenta mais uma vez se o sha
    ficou obsoleto por uma gravação concorrente (HTTP 409)."""
    for tentativa in range(2):
        dados, sha = await buscar_arquivo(projeto)
        dados = mutar(dados)
        resposta = await publicar_arquivo(projeto, dados, sha, mensagem)
        if resposta.status_code in (200, 201):
            return
        if resposta.status_code == 409 and tentativa == 0:
            continue
        raise HTTPException(502, "Falha ao publicar no GitHub.")
    raise HTTPException(502, "Conflito ao publicar, tente novamente em alguns segundos.")


app = FastAPI(title="Fórum das dissertações - API ponte compartilhada")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def healthcheck():
    return {"ok": True}


@app.post("/perguntas")
async def criar_pergunta(payload: NovaPergunta, request: Request):
    if payload.site:
        return {"ok": True}  # honeypot preenchido: finge sucesso e ignora
    checar_rate_limit(request.client.host if request.client else "desconhecido")

    projeto = resolver_projeto(payload.projeto, payload.topico)
    pergunta = sanitizar(payload.pergunta, 500)
    if not pergunta:
        raise HTTPException(400, "Pergunta vazia.")
    nome = sanitizar(payload.nome, 60) or "Anônimo"

    nova_pergunta = {
        "id": uuid.uuid4().hex[:10],
        "pergunta": pergunta,
        "autor": nome,
        "data": datetime.now(timezone.utc).isoformat(),
        "respostas": [],
    }

    def mutar(dados: dict) -> dict:
        dados.setdefault(payload.topico, []).append(nova_pergunta)
        return dados

    await commitar_mudanca(projeto, mutar, f"Fórum: nova pergunta em {payload.topico}")
    return {"ok": True}


@app.post("/respostas")
async def criar_resposta(payload: NovaResposta, request: Request):
    if payload.site:
        return {"ok": True}
    checar_rate_limit(request.client.host if request.client else "desconhecido")

    projeto = resolver_projeto(payload.projeto, payload.topico)
    resposta_txt = sanitizar(payload.resposta, 1000)
    if not resposta_txt:
        raise HTTPException(400, "Resposta vazia.")
    nome = sanitizar(payload.nome, 60) or "Anônimo"

    nova_resposta = {
        "id": uuid.uuid4().hex[:10],
        "texto": resposta_txt,
        "autor": nome,
        "data": datetime.now(timezone.utc).isoformat(),
    }

    def mutar(dados: dict) -> dict:
        perguntas = dados.get(payload.topico, [])
        for p in perguntas:
            if p.get("id") == payload.pergunta_id:
                p.setdefault("respostas", []).append(nova_resposta)
                return dados
        raise HTTPException(404, "Pergunta não encontrada.")

    await commitar_mudanca(projeto, mutar, f"Fórum: nova resposta em {payload.topico}")
    return {"ok": True}
