---
name: "ACCESSIBILITY_GUIDELINES"
description: "Accessibility guidelines for Next.js and React."
---

# Accessibility Guidelines (WCAG 2.2 AAA Focus)

A acessibilidade não é um plugin; é a fundação do nosso código. O Jornalista Inclusivo foi projetado para ser uma referência em design universal.

## 1. Navegação por Teclado

- Todos os elementos interativos devem ter um estado de `:focus-visible` explícito.
- **Padrão de Focus:** `focus:outline-none focus-visible:ring-2 focus-visible:ring-neutral-900 focus-visible:ring-offset-2 rounded-sm`.
- A ordem do DOM deve corresponder estritamente à ordem visual.
- Elementos ocultos visualmente (como o menu mobile fechado) devem receber `tabIndex="-1"` ou `inert` para evitar que o teclado navegue por eles.

## 2. Leitores de Tela (Screen Readers)

- Uso rigoroso de HTML semântico (`<article>`, `<nav>`, `<main>`, `<aside>`, `<time>`, `<header>`, `<footer>`).
- Botões que contêm apenas ícones DEVEM ter `aria-label` ou texto `.sr-only`.
  - Exemplo: `<button aria-label="Reproduzir áudio"><Play aria-hidden="true" /></button>`.
- Regiões dinâmicas (como o status de geração de áudio da IA) devem usar `aria-live="polite"` ou `aria-live="assertive"`.
- Ocultar ícones decorativos com `aria-hidden="true"`.

## 3. Imagens e Alt Text

- Todas as imagens editoriais utilizam o componente `<AutoAltImage>`.
- O Alt Text deve ser descritivo, contextual e não redundante (não iniciar com "Imagem de..." ou "Foto de...").
- Imagens puramente decorativas devem receber `alt=""` e `aria-hidden="true"`.

## 4. Redução de Movimento (Prefers-Reduced-Motion)

- Animações (como o slide-in do sticky player ou fade-ins) devem ser desativadas ou reduzidas se o usuário tiver a preferência ativada no SO. (Implementação via Tailwind `motion-reduce:` ou Framer Motion `useReducedMotion`).

## 5. Contraste e Cor

- Contraste mínimo de **7:1 (AAA)** para corpo de texto.
- Contraste mínimo de **4.5:1 (AA)** para textos grandes e componentes de UI.
- Nenhuma informação deve ser transmitida exclusivamente pela cor.

## 6. Modo Foco Profundo

- O "Reader Intelligence Mode" é uma feature de acessibilidade cognitiva, projetada para usuários com TDAH, autismo ou fadiga visual.
- Ele reduz o brilho, o contraste excessivo, e oculta distrações periféricas.
