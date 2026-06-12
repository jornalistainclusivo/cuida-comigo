# Cuida Comigo

> O Cuida Comigo é uma plataforma de gestão compartilhada projetada para descentralizar a carga cognitiva e operacional de cuidadores informais.

## Quick Start

O sistema é dividido em dois serviços principais: um *frontend* em Next.js e um *backend* em FastAPI (Python).

### Rodando o Backend (Python)
Abra o terminal, ative o ambiente virtual e inicie o servidor local:
```powershell
cd python_service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
A API estará disponível em `http://localhost:8000`.

### Rodando o Frontend (Next.js)
Abra uma nova aba no terminal e inicie o servidor de desenvolvimento:
```powershell
cd frontend
npm run dev
```
O frontend estará disponível em `http://localhost:3000`.

## Features MVP (v0.2-Alpha)

- **Coordenação Familiar:** Distribuição de tarefas assíncronas em um Círculo de Cuidado (*CareGroup*).
- **Gestão de Medicamentos:** Rastreabilidade de administração e controle de estoque de fármacos (*MedicationProtocol*).

## Configuration

As configurações e variáveis de ambiente devem ser alocadas em seus respectivos arquivos `.env` nos serviços `frontend` e `python_service`.

## Documentação

- [Arquitetura e Entidades](./ARCHITECTURE.md)
- [Estrutura do Projeto (Codebase)](./CODEBASE.md)
- [Acessibilidade (WCAG 2.2 AAA)](./docs/ACCESSIBILITY.md)
- [DevOps e Segurança](./docs/DEVOPS_AND_SECURITY.md)

## License

MIT
