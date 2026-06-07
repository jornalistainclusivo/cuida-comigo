---
name: "strapi5-ast-blocks"
description: "Reference guide for Strapi 5 AST block structures and data transformation protocols."
---

# Strapi 5 Abstract Syntax Tree (AST) Reference

**Status:** Obrigatório para `Contextual_Layer` e `Dynamic Zones`.

Este documento estabelece o padrão de intercâmbio de dados entre o Motor de IA e o Strapi 5. O Strapi 5 utiliza o formato **JSON Blocks**, uma estrutura de árvore que substitui o Markdown rudimentar.📘

---

## 🚫 A Regra de Ouro: O Banimento do Markdown

É terminantemente proibida a injeção de strings formatadas via Markdown (ex: `**bold**`, `[link](url)`, `### Heading`).

- **Falha:** Retornar `{"text": "**Capacitismo** é..."}` resultará em erro de renderização no Frontend.
- **Sucesso:** Decompor a formatação em objetos de texto com atributos booleanos.

---

## 🌳 Arquitetura de Nós (Nodes)

### 1. Parágrafo Padrão (Base)

Todo bloco de texto deve ser encapsulado em um objeto de nível superior com o tipo `paragraph`.

```json
[
  {
    "type": "paragraph",
    "children": [
      {
        "type": "text",
        "text": "Conteúdo textual sem estilização."
      }
    ]
  }
]
```

### 2. Formatação Granular (Inline Styles)

Estilizações (Negrito, Itálico, Código) devem ser propriedades booleanas dentro do nó de texto.

```json
{
  "type": "paragraph",
  "children": [
    { "type": "text", "text": "O termo " },
    { "type": "text", "text": "Capacitismo", "bold": true },
    { "type": "text", "text": " é o foco deste glossário." }
  ]
}
```

### 3. Links e Referências

Links são nós de nível médio que possuem seu próprio array de `children`.

```json
{
  "type": "link",
  "url": "[https://jinc.com.br/acessibilidade](https://jinc.com.br/acessibilidade)",
  "children": [{ "type": "text", "text": "Saiba mais", "italic": true }]
}
```

---

## 📝 Instrução para `ai-prompts.ts` (System Instruction)

Para garantir que a Skill `strapi-editorial-orchestrator` produza outputs válidos, os prompts devem conter a seguinte cláusula de restrição:

> "Você é um gerador de conteúdo para Strapi 5 Blocks. PROIBIDO o uso de sintaxe Markdown. O output deve ser um ARRAY JSON estrito de objetos. Cada objeto deve seguir a interface AST: `{ type: 'paragraph' | 'heading' | 'list', children: Array<{ type: 'text', text: string, bold?: boolean, italic?: boolean }> }`. Se o campo for um link, use `{ type: 'link', url: string, children: [...] }`."

---

## 🧪 Validação de Output

Qualquer script de validação (`checklist.py`) deve verificar:

1. Se a raiz do campo `description` é um `Array`.
2. Se todos os objetos possuem a chave `type`.
3. Se o texto real está exclusivamente dentro da chave `text` de um nó filho.
