---
trigger: always_on
---

# 🛡️ DevOps JINC Protocol: AI-Native Hybrid Governance

Este protocolo estabelece as diretrizes mandatórias de engenharia para a colaboração entre o Arquiteto Humano e os Agentes de IA na organização **Jornalista Inclusivo (JINC Apps)**.

## 1. O Motor Agêntico (Rules of Engagement)

O agente de IA operando neste repositório **deve** internalizar este comportamento estrutural:

- **Zero-Hallucination Policy:** Se uma biblioteca, dependência ou versão do Next.js/React não possuir uma funcionalidade nativa, o agente DEVE alertar o humano. Proibido inventar APIs ou _polyfills_ inseguros.
- **Security by Default:** Arquivos de ambiente (`.env*`), chaves de API, tokens e senhas NUNCA devem ser adicionados ao _stage_ do Git. O agente deve sugerir a inclusão em `.gitignore` pró-ativamente.
- **Agnosticismo de Estado Lógico:** Questione ambiguidades de arquitetura antes de escrever a primeira linha de código. Use o comando `/plan` compulsoriamente para _features_ complexas.

## 2. Padrões de Engenharia Full-Stack & DevOps

### 2.1 Arquitetura Next.js / React

- **Server-First:** Priorizar React Server Components (RSC) para redução de bundle JavaScript. Usar a diretiva `"use client"` estritamente nas bordas da árvore de componentes (interatividade ou estado).
- **Data Fetching:** Implementar ISR (Incremental Static Regeneration) ou cache revalidado por _tags_ para otimização de performance no Edge.
- **Observabilidade:** Todo bloco `try/catch` de funções críticas deve gerar logs estruturados e telemetria, não apenas `console.error`.

### 2.2 Segurança de Infraestrutura (Zero-Trust)

- **Sanitização de Inputs:** Nunca confiar no input do cliente ou do servidor. Validar dados com esquemas robustos (ex: Zod) no nível da API e de _Server Actions_.
- **Docker Multi-Stage:** Imagens de contêineres devem ser _multi-stage_, utilizando distroless ou Alpine mínimas para produção, reduzindo a superfície de ataque.
- **Supply Chain:** Sugerir rodar `npm audit` ou ferramentas de escaneamento de vulnerabilidade (SAST/DAST) após adições significativas de dependências.

## 3. Preservação de Estado e Higiene de Ambiente

A autonomia do agente exige limites estritos de contenção para evitar degradação de repositório e vazamento de dados.

### 3.1 Versionamento Perpétuo (Git Tags)

Para garantir a recuperação perpétua de estados funcionais durante o Vibe-Coding, é **obrigatório** o uso de Git Tags a cada ciclo de desenvolvimento.

- **Nomenclatura Híbrida:** O padrão combina Versionamento Semântico com o escopo da branch: `v[Major].[Minor].[Patch]-[nome-da-branch]`.
- **Execução Mandatória:** Antes da fusão, o agente ou desenvolvedor deve gerar:

1. `git tag -a vX.X.X-branch-name -m "feat: implementação concluída e validada"`
2. `git push origin vX.X.X-branch-name`

### 3.2 Higiene de Ambiente Local (Sanitização)

Antes de encerrar uma sessão de desenvolvimento, o ambiente deve ser higienizado.

- **Limpeza de Artefatos:** Remover diretórios de build temporários e logs contaminados, preservando estritamente ambientes virtuais configurados (`.venv` em diretórios de serviços Python não devem ser corrompidos).
- **Comando de Higienização (Checklist Local):**

```bash
# Script mandatório: sanitize-local.sh
echo "🧹 Higienizando ambiente sob protocolo Zero-Trust..."
# Limpeza de builds e logs; .venv e dotfiles sensíveis são preservados
rm -rf .next/ coverage/ dist/ build/ *.log
git stash push -m "wip: backup automático pre-higienização" --include-untracked
npm cache verify
echo "✅ Ambiente sanitizado. Valide o git status antes de commitar."

```

## 4. Fluxo de Trabalho Híbrido (The JINC SDLC)

1. **Intenção (Humano):** Define o "quê" e o "porquê".
2. **Mapeamento & Segurança (IA):** Avaliação de dependências e riscos (Shift-Left).
3. **Prototipagem de Acessibilidade (IA):** Construção do esqueleto HTML semântico e marcações WAI-ARIA **antes** do CSS e lógica JS.
4. **Execução (H+IA):** Implementação lógica focada no Design System Neutro e performance (Core Web Vitals).
5. **Validação & Higienização (IA):** Execução do `sanitize-local.sh`, scripts de linting e geração da Git Tag de segurança.
6. **Geração do Contrato (IA):** Preenchimento final do PR Template estruturado.

---

## 🏗️ 5. Pull Request Contract (Saída Mandatória)

_Ao finalizar uma branch, o agente DEVE compilar o resultado neste template exato:_

```markdown
# 🤖 [TIPO]: Descrição Concisa (Ex: feat: implementa camada de cache ISR)

## 📝 Resumo do Contexto

[Explicação técnica e links para ADRs, se aplicável].

## 🔗 Issue / Ticket

Ref: #000

## 🏷️ Escopo de Mudança (Selecione)

- [ ] `a11y`: Acessibilidade (Sensorial ou Cognitiva).
- [ ] `sec`: Correção/Aprimoramento de Segurança.
- [ ] `infra`: Docker, CI/CD, ISR, Deploy.
- [ ] `feat`: Nova funcionalidade.
- [ ] `fix`: Correção de bug.
- [ ] `refactor`: Limpeza de código/Design System.

---

## ♿ Auditoria de Inclusão (WCAG 2.2 AAA & Cognitive)

- [ ] **Navegação:** Teclado funcional mapeado, sem _keyboard traps_.
- [ ] **Foco:** Visível (`focus-visible:ring-2`) em elementos interativos.
- [ ] **Semântica ARIA:** Aplicada conforme diretrizes do W3C.
- [ ] **Contraste & Cor:** Proporção 7:1 (AAA). Zero dependência exclusiva de cor.
- [ ] **Imagens & Fallbacks:** `<AutoAltImage>` implementado.
- [ ] **Cognição:** Respeito a `prefers-reduced-motion`.

## 🏛️ Design System Neutro & CWV

- [ ] **Paleta:** Uso exclusivo do espectro `neutral-50` a `neutral-900`.
- [ ] **Métricas CWV:** LCP otimizado, sem CLS indesejado.
- [ ] **Tipografia:** `font-serif` para conteúdo; `font-sans` para UI. Limite de `max-w-[70ch]`.

## 🛠️ DevOps, Higiene & Zero-Trust

- [ ] **Secrets:** Ausência absoluta de credenciais. `.env` não versionado.
- [ ] **Higiene Local:** Script `sanitize-local.sh` executado. Nenhuma contaminação cruzada.
- [ ] **Docker:** Build multi-stage testado (se aplicável).
- [ ] **Versionamento:** Git Tag Semântica gerada e em remote (`git push origin vX.X.X`).

## 🧪 Plano de Teste e Rollback

1. Comandos para teste: `git fetch && git checkout <branch> && npm run dev`
2. URL esperada: `http://localhost:3000/...`
3. **Plano de Rollback:** Reverter tag/commit `XXXXX` se as métricas falharem.
```

---

## 6. Comandos de Operação Especiais (Agent Slash Commands)

O agente reconhece e prioriza as seguintes diretivas no chat:

- `/plan <objetivo>`: Interrompe execução. Lista etapas técnicas, dependências e riscos antes de codificar.
- `/audit`: Dispara revisão silenciosa buscando vulnerabilidades OWASP, vazamento de memória e quebras WCAG.
- `/refactor`: Reescreve o bloco focado em modularização, extração de Server Components e simplificação ciclomática.
- `/status`: Avalia o git diff contra a intenção original, identificando pendências da sprint.
- `/sanitize`: Executa imediatamente os protocolos de higiene de ambiente descritos na seção 3.2.
