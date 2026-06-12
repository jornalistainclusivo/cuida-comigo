# Mapa da Codebase

> Guia para navegação nas pastas e dependências do repositório Cuida Comigo.

## Estrutura de Diretórios

- **`.agents/`**: Contém o JINC Protocol, definições de agentes LLM, scripts automatizados (como `sdd_validator.py` e `checklist.py`) e fluxos de trabalho (Workflows).
- **`specs/`**: Contém os contratos do *Specification-Driven Development* (PRD e Tech Specs). Toda nova funcionalidade deve primeiro ser formalizada aqui e passar no validador SDD.
- **`frontend/`**: Aplicação Next.js (TypeScript, React). Contém `src/` (componentes e rotas), `public/` (ativos estáticos) e as configurações vitais (`next.config.ts`, `eslint.config.mjs`).
- **`python_service/`**: API FastAPI (Python). Contém `app/` (rotas `main.py`, `models.py`, `schemas.py`, `database.py`), `tests/` (Pytest), e `migrations/` (Alembic para controle de esquemas do DB).
- **`docs/`**: Documentações específicas sobre DevOps, Segurança e Acessibilidade.

## Gerenciamento de Dependências

- Frontend: Gerenciado via `npm` (`package.json` / `package-lock.json`).
- Backend: Gerenciado via ambiente virtual `venv` e pacotes listados no `requirements.txt`.
