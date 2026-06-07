---
name: "ACCESSIBILITY"
description: "Accessibility guidelines for Next.js and React."
---

# ♿ Manifesto de Acessibilidade: Jornalista Inclusivo

Este documento define os padrões rigorosos de acessibilidade (A11y) que o projeto **Jornalista Inclusivo** deve seguir. O objetivo não é apenas "passar nos validadores", mas oferecer uma experiência de navegação superior para todos os usuários.

**Meta:** WCAG 2.2 Nível AAA (onde tecnicamente viável), mínimo AA obrigatório.

## 1. Diretrizes Visuais e de Design

### 🎨 Cores e Contraste

O esquema de cores foi selecionado para garantir legibilidade máxima.

- **Texto Normal:** Contraste mínimo de **4.5:1** (AA) e idealmente **7:1** (AAA).
- **Texto Grande (18pt+ ou 14pt bold):** Contraste mínimo de **3:1** (AA) e idealmente **4.5:1** (AAA).
- **Elementos de Interface (Ícones, Bordas de Input):** Contraste mínimo de **3:1**.

**Paleta Acessível:**

- Fundo: `#FFFFFF` (Branco) ou `#F5F5F7` (Off-white para conforto visual)
- Texto Principal: `#141414` (Preto Suave - nunca preto absoluto `#000` em fundo branco para evitar vibração)
- Azul Institucional (Links/Botões): `#1F3FA3` (Verificado: Contraste 8.8:1 sobre branco - **Aprovado AAA**)
- Azul Escuro (Headings): `#142B70` (Verificado: Contraste 13.5:1 sobre branco - **Aprovado AAA**)

### 🔠 Tipografia

- **Fontes:** Inter (Sans) e JetBrains Mono (Mono).
- **Tamanho Base:** 16px (1rem). Nunca definir tamanhos fixos em `px` para containers de texto; usar `rem` para permitir escalabilidade pelo navegador.
- **Entrelinha (Line Height):** Mínimo de 1.5 para texto corrido.
- **Parágrafos:** Largura máxima de 80 caracteres (aprox. `max-w-prose` ou `65ch`) para evitar fadiga de leitura.

## 2. Implementação Técnica (Dev Guidelines)

### ⌨️ Navegação por Teclado

- **Foco Visível:** O outline de foco (`ring`) nunca deve ser removido (`outline: none`) sem uma substituição clara e de alto contraste.
- **Ordem de Tabulação:** Deve seguir a ordem lógica visual.
- **Skip Links:** Obrigatório no topo da página: "Pular para o conteúdo principal".

### 🖼️ Imagens e Mídia

- **Imagens Decorativas:** `alt=""` (vazio) ou `aria-hidden="true"`.
- **Imagens Informativas:** `alt` descritivo que transmite o _conteúdo_ e a _função_ da imagem, não apenas a aparência.
- **Gráficos/Infográficos:** Devem ter uma descrição longa (`longdesc` ou texto adjacente) acessível.

### 🏗️ Semântica HTML

- **Headings:** Hierarquia estrita (`h1` > `h2` > `h3`). Nunca pular níveis (ex: de `h2` para `h4`).
- **Landmarks:** Uso correto de `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` para permitir navegação rápida por leitores de tela.
- **Botões vs Links:**
  - Vai para outra página? Use `<a>` (Link).
  - Executa uma ação na mesma página? Use `<button>`.

## 3. Ferramentas Assistivas Integradas

O site deve fornecer controles nativos para o usuário ajustar a experiência:

1. **High Contrast Toggle:** Inverte cores ou aplica tema de alto contraste (Fundo Preto / Texto Amarelo ou Branco).
2. **Font Resizer:** Aumenta o tamanho da fonte base sem quebrar o layout.
3. **Dyslexia Font (Opcional):** Opção para trocar a fonte por OpenDyslexic ou similar.
4. **Motion Reduction:** Respeitar `prefers-reduced-motion`. Se o usuário preferir menos movimento, desativar animações de entrada e transições bruscas.

## 4. Checklist de Validação (Definition of Done)

Antes de qualquer deploy, a página deve passar por:

- [ ] Validação automática (Lighthouse / Axe DevTools) com score 100.
- [ ] Teste manual de navegação apenas com teclado (Tab, Enter, Space, Esc).
- [ ] Teste com leitor de tela (NVDA no Windows ou VoiceOver no Mac) para verificar a verbosidade e clareza dos rótulos.
- [ ] Verificação de zoom de 200% sem perda de funcionalidade ou sobreposição de texto.

---

> "Acessibilidade não é uma feature, é um direito."
