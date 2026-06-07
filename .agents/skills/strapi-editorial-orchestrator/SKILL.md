---
name: strapi-editorial-orchestrator
description: How to process journalistic drafts in Strapi 5 and generate AI metadata, Plain Language summaries, and Contextual Layers. Make sure to use this skill whenever the user mentions `/automacao-jinc`, `/revisar-acessibilidade`, `/gerar-contexto`, "Strapi 5 lifecycles", "AST Blocks", "Plain Language WCAG", "Gerar SEO", or is editing files like `lifecycles.ts` or `ai-prompts.ts` in the CMS. Even if they don't explicitly name this skill, trigger it when dealing with Strapi 5 AI metadata generation or accessible journalistic content processing.
---

# 🎼 Orquestrador Editorial Inteligente para Strapi 5

Esta skill habilita a capacidade de **Engenharia Editorial Autônoma**. Ela orienta a IA para atuar como um Editor de Acessibilidade e SEO de alto nível, operando diretamente nos ciclos de vida (_lifecycles_) e utilitários de prompt do Strapi 5. O foco é a transformação de rascunhos fragmentados em artefatos jornalísticos estruturados e acessíveis.

## 🎯 Escopo de Atuação Técnica

Ao ativar esta skill, o agente deve priorizar a implementação e refatoração de lógica nos seguintes domínios:

### 1. Processamento de Acessibilidade (WCAG 2.2 AAA)

- **Visão Computacional & Descrição:** Consolidar metadados de mídia para gerar `alt_text_ia` (objetivo, máx. 125 chars) e `descricao_audio` (narrativo e imersivo).
- **Linguagem Simples (Plain Language):** Sintetizar blocos de `Texto_Livre` no campo `resumo_simples`, aplicando o limite estrito de **45 palavras** e ordem direta (S+V+P).

### 2. Engenharia de Contexto Dinâmico (AST Blocks)

- **Extração Semântica:** Analisar a massa de dados do rascunho (Texto + Quotes + Categorias) para identificar jargões técnicos.
- **Injeção de Glossário:** Compor o componente `Contextual_Layer` respeitando a árvore **AST (Abstract Syntax Tree)** do Strapi 5, evitando terminantemente a injeção de Markdown.

### 3. Autoridade e Visibilidade (E-E-A-T & SEO)

- **Metadados Estruturados:** Gerar o objeto `SEO` (`metaTitle`, `metaDescription`, `keywords`) com base no valor jornalístico e factual do conteúdo, garantindo conformidade com as diretrizes de busca orgânica.

---

## 🧠 Protocolos de Robustez (SDD - Spec-Driven Development)

Para garantir que a automação não corrompa o banco de dados ou interrompa o serviço:

- **Sanitização de Payload:** Todo retorno de LLM (especialmente via Groq/LLaMA) deve passar por limpeza via Regex: `response.replace(/```json|```/g, '')` antes do `JSON.parse`.
- **Prevenção de Recursividade:** Implementar flags de controle nos lifecycles (`beforeUpdate`) para garantir que a atualização disparada pela IA não acione o mesmo gatilho infinitamente.
- **Fail-Safe Editorial:** Em caso de erro na API de IA, o sistema deve registrar o log e permitir o salvamento do rascunho original sem os metadados automáticos, priorizando a disponibilidade do CMS.

---

## 📂 Divulgação Progressiva (Context Loading)

> [!CAUTION]
> **Otimização de Performance:** O sistema de blocos do Strapi 5 é complexo. Carregue referências estendidas apenas sob demanda.

- **Se a tarefa envolver:** Escrever, injetar ou validar nós no `Contextual_Layer` ou qualquer Dynamic Zone que utilize **JSON Blocks/AST** nativos:
  - **VOCÊ DEVE LER:** `.agent/skills/strapi-editorial-orchestrator/references/strapi5-ast-blocks.md`.

---

## 📝 Regras de Ouro para `ai-prompts.ts`

Ao construir ou editar prompts nesta biblioteca:

1. **Consolidação de Contexto:** Nunca envie apenas o título. O prompt deve ser instruído a ler o `payload` completo (Texto + Citações + Capa).
2. **Instruções Negativas:** Use ênfase em restrições: "PROIBIDO usar Markdown", "LIMITE ESTRITO de 45 palavras".
3. **Few-Shot Examples:** Sempre inclua um exemplo do JSON esperado para moldar a probabilidade do output da IA.

## 🧪 Validação e Evals

Após qualquer modificação:

- Execute `npm run build` no CMS para validar a tipagem do TypeScript.
- Utilize o arquivo `evals/evals.json` para testar se a lógica de extração suporta casos de borda (textos muito curtos ou excesso de jargões).
- Verifique se os campos críticos (`alt_text_ia`, `resumo_simples`, `metaTitle`) estão sendo populados corretamente no banco de dados.

---

### 🔍 Próximos Passos para o Agente

1. Validar se o arquivo `references/strapi5-ast-blocks.md` existe e está atualizado.
2. Analisar o `lifecycles.ts` atual para identificar onde plugar a nova orquestração editorial sem quebrar as funções de `alt_text` existentes.
3. Reportar ao usuário qualquer inconsistência entre os tipos do Strapi e as interfaces do Frontend.
