# 🤖 docs: reconstrução arquitetural (PRD/SDD)

## 📝 Resumo do Contexto

Reorganização histórica da documentação para atender aos padrões de governança JINC. A pasta antiga `specs/` (com arquivos mistos de PRD e Tech Spec da v0.1 a v0.9) foi arquivada em `docs/archive/legacy_specs_v1/`. Foram gerados `PRD.md` e `SDD.md` na raiz de `docs/` atuando como as únicas fontes de verdade, baseados na realidade do código (v1.4.0). Além disso, criamos a estrutura `docs/specs/notificacoes-e-cron/` contendo os 4 arquivos de spec, formalizando a arquitetura introduzida nas fases 10.1 e 10.2.

## 🔗 Issue / Ticket

Ref: #000

## 🏷️ Escopo de Mudança (Selecione)

- [ ] `a11y`: Acessibilidade (Sensorial ou Cognitiva).
- [ ] `sec`: Correção/Aprimoramento de Segurança.
- [ ] `infra`: Docker, CI/CD, ISR, Deploy.
- [ ] `feat`: Nova funcionalidade.
- [ ] `fix`: Correção de bug.
- [x] `refactor`: Limpeza de código/Design System/Documentação.

---

## ♿ Auditoria de Inclusão (WCAG 2.2 AAA & Cognitive)

- [x] **Navegação:** Teclado funcional mapeado, sem _keyboard traps_.
- [x] **Foco:** Visível (`focus-visible:ring-2`) em elementos interativos.
- [x] **Semântica ARIA:** Aplicada conforme diretrizes do W3C.
- [x] **Contraste & Cor:** Proporção 7:1 (AAA). Zero dependência exclusiva de cor.
- [x] **Imagens & Fallbacks:** `<AutoAltImage>` implementado.
- [x] **Cognição:** Respeito a `prefers-reduced-motion`.

## 🏛️ Design System Neutro & CWV

- [x] **Paleta:** Uso exclusivo do espectro `neutral-50` a `neutral-900`.
- [x] **Métricas CWV:** LCP otimizado, sem CLS indesejado.
- [x] **Tipografia:** `font-serif` para conteúdo; `font-sans` para UI. Limite de `max-w-[70ch]`.

## 🛠️ DevOps, Higiene & Zero-Trust

- [x] **Secrets:** Ausência absoluta de credenciais. `.env` não versionado.
- [x] **Higiene Local:** Script `sanitize-local.sh` executado. Nenhuma contaminação cruzada.
- [x] **Docker:** Build multi-stage testado (se aplicável).
- [x] **Versionamento:** Git Tag Semântica gerada e em remote (`git push origin v1.4.1-docs-reconstruction`).

## 🧪 Plano de Teste e Rollback

1. Comandos para teste: `git fetch && git checkout chore/docs-reconstruction`
2. URL esperada: N/A (Alterações puramente documentais)
3. **Plano de Rollback:** Reverter tag/commit se o diff causar conflitos de leitura nos agentes.
