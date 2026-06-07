---
name: jinc-governance-standards
description: 🛡️ JINC Governance Standards — DevOps & Vibe-Coding Edition. Mandatory guidelines for accessibility, inclusion, and ethics for the Jornalista Inclusivo project.
version: 2.0.0
status: Knowledge-Ready
domain:
  name: JINC Apps
  parent_entity: JornalistaInclusivo.com
  mission: Engenharia para Jornalismo Acessível e Diverso
infrastructure:
  host_os: Windows 11
  subsystem: Ubuntu (WSL2)
  deploy: Cloud Dev Environments
collaboration:
  mode: Human + AI Co-Creation
  methodology: Vibe-Coding (Intent-Based Development)
core_values:
  - Rigor Jornalístico e Checagem
  - Ética e Direitos Humanos
  - Equidade, Inclusão e Representatividade
---

# 🛡️ JINC Apps: Governança de Engenharia Inclusiva

Este documento define as regras operacionais, éticas e técnicas para o desenvolvimento de software na iniciativa JINC Apps. Agentes de IA e colaboradores humanos devem aderir estritamente a estas diretrizes.

---

## 0. Princípios Fundamentais

### 0.1 Engenharia como Extensão Ética

O código JINC é uma manifestação funcional da Declaração Universal dos Direitos Humanos e da Ética Jornalística.

- **Mandatário:** Conformidade com Direitos Humanos, inclusão radical, representatividade interseccional, rigor informacional e transparência técnica.

### 0.2 Accessibility as Infrastructure

Acessibilidade (A11y) é base arquitetural, não uma tarefa de QA.

- **Regra:** Qualquer commit que degrade métricas de acessibilidade ou falhe nos protocolos WCAG 2.2 AAA é um erro crítico impeditivo (blocker).

### 0.3 Integridade de Dados Jornalísticos

Sistemas devem suportar padrões de redação profissional:

- Verificação de fontes, versionamento editorial imutável, rastreabilidade de mudanças (GitOps) e preservação histórica.

---

## 1. Modelo Operacional DevOps (GitOps + Vibe Flow)

### 1.1 Estratégia de Branching

- **main:** Protegida. Apenas via Pull Request.
- **feat/_, fix/_, docs/_, hotfix/_:** Branches efêmeras para desenvolvimento.
- **Proibido:** Commits diretos na `main`.

### 1.2 Protocolo de Sincronização (Linear History)

1. `git fetch origin`
2. `git pull origin main`
3. `git rebase main` (Garantir histórico limpo para auditoria editorial).

### 1.3 Semântica de Commit

Padrão _Conventional Commits_ com extensões JINC:

- **ethics:** Mudanças em regras editoriais ou algoritmos de diversidade.
- **a11y:** Mudanças estruturais de acessibilidade.
- Outros: `feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `sec:`.

---

## 2. Governança de IA (Colaboração Humano-Agente)

### 2.1 Regras de Comportamento

- **Anti-Generic UI:** Rejeitar estéticas padrão de mercado. UI deve ser editorial.
- **Linguagem Inclusiva:** Uso obrigatório de termos inclusivos (PT-BR) sem perda de clareza.
- **Explicabilidade:** Agentes devem justificar decisões de arquitetura ética.

### 2.2 The Purple Ban (Identidade Visual)

- **Proibido:** Roxo/Violeta dominante, gradientes "neon tech" e templates genéricos.
- **Contraste:** Alvo mínimo de **7:1 (WCAG AAA)**.

### 2.3 Firewall de Dados

- **Segredos:** Nunca versionar `.env`, `*.pem`, `api_keys.json`.
- **Privacidade:** Proibida a transmissão ou armazenamento de PII, dados médicos ou sensíveis de pessoas com deficiência (PcD).

---

## 3. Padrão de Engenharia de Acessibilidade

### 3.1 Baseline de Conformidade

- **WCAG 2.2 AAA** é o requisito mínimo não negociável.

### 3.2 Schema de Banco de Dados (Obrigatório)

```sql
-- Campos obrigatórios em tabelas de mídia/conteúdo
alt_text TEXT NOT NULL,
aria_label VARCHAR(255) NOT NULL,
long_description TEXT,
audio_version_url URL,
reading_level ENUM('basic', 'intermediate', 'advanced')
```

### 3.3 Sinais de Acessibilidade em Runtime

Sistemas devem reagir dinamicamente a: `prefers-reduced-motion`, `prefers-contrast`, `prefers-color-scheme` e detecção de navegação por teclado.

---

## 4. Integridade Jornalística no Software

### 4.1 Metadados Editoriais Mandatários

Todo conteúdo deve carregar: `source_name`, `source_url`, `doi_reference`, `fact_checked_by`, `last_verified_date`, `editorial_revision_history`.

### 4.2 Transparency Logging

Logs de alteração de conteúdo e correções editoriais devem ser **imutáveis**. A deleção de histórico editorial é estritamente proibida.

---

## 5. Ambiente de Desenvolvimento Seguro

### 5.1 Governança de Dependências

- Versões **LTS** apenas. Auditoria automática via `npm audit` ou `Snyk`.
- Lockfiles (`package-lock.json`) são obrigatórios para builds determinísticos.

### 5.2 Independência de ORM

Lógica de negócio desacoplada (Clean Architecture). ORMs (Prisma/Drizzle) atuam apenas como adaptadores. Regras éticas residem na camada de domínio (Pure TS).

---

## 6. Integração de Knowledge Items

### 6.1 Registro de Capacidades

Novas funções de IA/Skills devem ser registradas em `.agent/skills_index.json` e `.agent/knowledge_registry.json`.

### 6.2 Padrão de Documentação de Módulo

Todo módulo em `docs/` deve conter: `purpose.md`, `a11y.md`, `ethics.md`, `data_flow.md`.

---

## 7. Protocolo de Segurança Vibe-Coding

- **Antes de Codar:** Validar se a solução é inclusiva, auditável e acessível.
- **Durante a Codificação (Hierarquia):** Acessibilidade > Performance; Clareza > Estética; Segurança > Conveniência (DX).

---

## 8. DevOps Quality Gate (The Vibe Check)

Pipeline pré-merge obrigatório:

1. **Qualidade:** ESLint, Prettier, TSC (Zero erros).
2. **A11y Scan:** Axe-core / Pa11y (Zero violações AAA).
3. **Segurança:** Snyk / Dependabot (Zero vulnerabilidades High/Critical).
4. **Build:** `npm run build` (Zero warnings).

---

## 9. Protocolo de Ética em Incidentes

Bugs de acessibilidade ou direitos humanos têm **PRIORIDADE P0**. O lançamento de novas features deve ser pausado até a correção do hotfix ético.

---

## 10. Definition of Done (DoD)

Um item só está "Pronto" se: acessível por teclado, compatível com leitor de tela, fallback sem JS funcional, metadados editoriais completos e logs auditáveis gerados.

---

## 11. Cláusula de Engenharia Cultural

Priorizar sempre: **Humanidade > Velocidade** | **Inclusão > Tendência** | **Ética > Conveniência**.

---

## 12. Aplicação da Governança (Enforcement)

Violações resultam em bloqueio de merge, rollback automático e revisão arquitetural obrigatória.

---

## 13. Política de Versionamento

Padrão: `MAJOR.MINOR.PATCH-ETHICS`

- **ETHICS:** Mudança em políticas de inclusão ou padrões de direitos humanos.

---

## 14. Identidade Estratégica

A JINC Apps constrói software como instrumento de equidade, tecnologia como ferramenta de cidadania e infraestrutura como extensão do jornalismo.
