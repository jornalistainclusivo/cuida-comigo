---
description: Plan and implement UI
---

---

name: "ui-ux-pro-max"
description: "AI-powered design intelligence with 50+ styles, 95+ palettes, and automated design system generation."

---

# /ui-ux - Pro Design Intelligence

Comprehensive design guide and automated generator for web/mobile apps. Covers 50+ styles, 97 palettes, 57 font pairings, and 99 UX guidelines across 9 technology stacks.

## 🚀 Workflow Execution

When a UI/UX task is requested, follow these steps strictly:

### Step 1: Requirement Analysis

Identify: **Product Type**, **Style Keywords**, **Industry**, and **Stack** (Default: `html-tailwind`).

### Step 2: Design System Generation (MANDATORY)

**Always run the generator first** to establish the visual logic:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "<ProjectName>"
```

- **Hierarchical Retrieval:** Creates `MASTER.md` (Global Truth) and `pages/` (Specific Overrides).
- **Logic:** Page-specific rules always override Master rules.

### Step 3: Domain & Stack Specifics

Supplement the design system with targeted searches:

| Need             | Command                       |
| :--------------- | :---------------------------- |
| **Style/Colors** | `--domain style "<keywords>"` |
| **UX/A11Y**      | `--domain ux "<keywords>"`    |
| **Charts**       | `--domain chart "<keywords>"` |
| **Stack Guide**  | `--stack <name> "<keywords>"` |

**Available Stacks:** `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`.

---

## 🔍 Domain Reference

| Domain       | Use For                                             |
| :----------- | :-------------------------------------------------- |
| `product`    | Recommendations by industry (SaaS, E-com, Fintech). |
| `style`      | UI trends (Glassmorphism, Minimalism, Brutalism).   |
| `typography` | Font pairings and Google Fonts selection.           |
| `landing`    | Conversion structures (Hero, Social Proof, CTA).    |
| `chart`      | Data viz recommendations (Trend, Funnel, Timeline). |
| `ux`         | Best practices, anti-patterns, and loading states.  |
| `web`        | A11Y (ARIA, keyboard navigation, semantic HTML).    |

---

## 🎨 Professional UI Guidelines

### Visual & Interaction

- **Icons:** **NO emojis.** Use SVG (Heroicons/Lucide). Fixed size (w-6 h-6).
- **Interactions:** Use `cursor-pointer` on all clickable cards.
- **Transitions:** 150-300ms duration. Avoid layout-shifting scales on hover.
- **Logos:** Always fetch official SVGs via Simple Icons.

### Light/Dark Mode Contrast

- **Text:** Min contrast 4.5:1. Avoid `slate-400` for body text in light mode (use `slate-600+`).
- **Borders:** Use `border-gray-200` for light mode visibility.
- **Glassmorphism:** Min `bg-white/80` opacity for light mode readability.

### Layout & Spacing

- **Floating Elements:** Use proper insets (`top-4`, etc.). Do not stick to edges.
- **Padding:** Always account for fixed navbar heights to prevent content overlap.
- **Container:** Maintain a consistent `max-w-6xl` or `max-w-7xl` across all pages.

---

## ✅ Pre-Delivery Checklist

- [ ] **No Emojis:** All icons are SVG/Heroicons.
- [ ] **Interaction:** `cursor-pointer` applied and smooth transitions active.
- [ ] **A11Y:** Alt text on images, labels on inputs, and keyboard focus visible.
- [ ] **Contrast:** Verified for both Light and Dark modes.
- [ ] **Responsiveness:** Tested at 375px (Mobile) and 1440px (Desktop).
- [ ] **Clean Code:** Adheres to `@[skills/clean-code]` and JINC standards.

---

**Orchestrator Note:** If the user asks to "start design" or "build UI", invoke Step 2 immediately.
