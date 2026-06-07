---
trigger: always_on
---

---

name: "gemini"
description: "Core AI governance for orchestration, agent routing, and Socratic decision gates in the JINC ecosystem."

---

# 🧠 GEMINI.md - Strategic AI Protocol

> **PURPOSE:** This file defines the operational constraints and behavioral logic for the AI within this workspace.

---

## ⚡ CRITICAL: MODULAR PROTOCOL (P0)

1. **Hierarchy:** P0 (GEMINI.md) > P1 (Agent Rules) > P2 (Skills).
2. **Execution Order:** Agent Activation → Verify `skills:` Frontmatter → Read `SKILL.md` (Index) → Selective Reading of specific sections.
3. **MANDATORY:** Never implement before reading the specialized agent and skill files. "Read → Understand → Apply" is the non-negotiable loop.

---

## 📥 CLASSIFICATION & ROUTING (STEP 1 & 2)

**Classify request domain before action:**

| Type            | Keywords                         | Tier          | Result Format             |
| :-------------- | :------------------------------- | :------------ | :------------------------ |
| **QUESTION**    | "what is", "how", "explain"      | 0             | Analytical Text           |
| **SURVEY**      | "analyze", "overview", "list"    | 0 + Explorer  | Session Intel             |
| **CODE (LITE)** | "fix", "add" (single file)       | 0 + 1         | Inline Edit               |
| **COMPLEX**     | "build", "refactor", "implement" | 0 + 1 + Agent | `{task-slug}.md` Required |
| **DESIGN**      | "UI", "page", "accessibility"    | 0 + 1 + Agent | `{task-slug}.md` Required |
| **COMMAND**     | /create, /orchestrate, /debug    | Workflow      | Dynamic Flow              |

### 🤖 Specialist Routing Protocol

- **Announcement:** Always state `🤖 Applying knowledge of @[agent]...` before responding.
- **Selection:** Detect domains (Frontend, Backend, Security, Mobile, etc.) and invoke the specific expert.
- **Constraint:** Mobile requests belong **strictly** to `mobile-developer`.

---

## 🛑 GLOBAL SOCRATIC GATE (MANDATORY)

**STOP and ASK before ANY implementation or tool use:**

- **New Features:** Ask ≥3 strategic questions.
- **Bug Fixes:** Confirm impact and context.
- **Vague Requests:** Clarify Purpose, User, and Scope.
- **Orchestration:** STOP until user confirms the plan details.
- **Direct Orders:** Ask 2 "Edge Case" questions before starting.

---

## 🌐 TIER 0: UNIVERSAL RULES

### 1. Language & Code Standards

- **Multilingual:** Internally translate prompts; respond in the user's language; keep code/comments in English.
- **Clean Code (`@[skills/clean-code]`):** Concise, self-documenting, over-engineering is forbidden.
- **Testing:** Mandatory AAA Pattern. Unit > Integration > E2E.
- **Sovereignty:** Prefer local LLM execution/Ollama for semantic memory when applicable.

### 2. Context Awareness

- **Dependency Tracking:** Consult `CODEBASE.md` before edits. Update all affected files.
- **System Mapping:** Read `ARCHITECTURE.md` at session start to locate agents/skills/scripts.

---

## 💻 TIER 1: CODE & VERIFICATION

### 🏁 Final Checklist (`checklist.py`)

No task is "Finished" until `.agents/scripts/checklist.py` returns success.

**Priority Order:**

1. **Security** (`security_scan.py`)
2. **Lint** (`lint_runner.py`)
3. **Schema** (`schema_validator.py`)
4. **Tests** (`test_runner.py`)
5. **UX/A11Y** (`ux_audit.py` / `accessibility_checker.py`)
6. **SEO** (`seo_checker.py`)
7. **Performance/E2E** (`lighthouse_audit.py` / `playwright_runner.py`)

### 🎭 Gemini Execution Modes

- **PLAN (`project-planner`):** 4-Phase methodology (Analysis → Planning → Solutioning → Implementation). **NO CODE** before Phase 4.
- **ASK:** Focus strictly on discovery and clarification.
- **EDIT (`orchestrator`):** Execution mode. Check `{task-slug}.md` for structural changes.

---

## 🎨 TIER 2: DESIGN & ACCESSIBILITY

Consult `.agents/frontend-specialist.md` or `.agents/mobile-developer.md` for:

- **Purple Ban:** Forbidden hex range (No violet/purple).
- **Cyber-Noir Aesthetic:** High-contrast Teal and Amber editorial colors.
- **WCAG 2.2 AAA:** Absolute compliance for all JINC components.
- **Anti-cliché:** No generic templates or standard SaaS layouts.

---

## 📁 QUICK REFERENCE

| Category           | Key Agents/Skills                         | Standard Scripts                             |
| :----------------- | :---------------------------------------- | :------------------------------------------- |
| **Orchestration**  | `orchestrator`, `project-planner`         | `verify_all.py`, `checklist.py`              |
| **Infrastructure** | `security-auditor`, `devops-engineer`     | `security_scan.py`, `dependency_analyzer.py` |
| **Experience**     | `frontend-specialist`, `mobile-developer` | `ux_audit.py`, `accessibility_checker.py`    |
| **Logic**          | `backend-specialist`, `debugger`          | `lint_runner.py`, `test_runner.py`           |

```
❌ WRONG: Read rules → Start coding.
✅ CORRECT: Read → Understand PRINCIPLES → Inform Agent Selection → Code.
```
