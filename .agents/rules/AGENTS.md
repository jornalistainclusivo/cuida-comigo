---
trigger: always_on
---

---

name: "agents-governance"
description: "Global behavioral guidelines and persona definitions for JINC agents."

---

# Antigravity Agent Configurations

## Permissions

- Allow execution of Python scripts within `.agents/scripts/`
- Allow npm commands for dependency management
- Allow read/write access to `src/` and `lib/`

## Skill Mapping

- Terminal: Enabled (via Terminal Integration v1.22.2)
- Filesystem: Restricted to workspace

## Tool Authorizations

- **`Bash` Tool:** Authorized for the agents `orchestrator`, `powershell-windows`, `seo-specialist`, `backend-specialist`, `database-architect`, `debugger`, `devops-engineer`, `qa-automation-engineer`, `project-planner`, `product-owner`, `product-manager`, `performance-optimizer`, `penetration-tester`, `mobile-developer`, `game-developer`, `frontend-specialist`, `explorer-agent`, `documentation-writer`, `security-auditor`, and `test-engineer`.
- **Scope:** Restricted to project directories.

## Security Protocol

- The agent must request confirmation before executing `npm install` if there are changes in `package-lock.json`.
- Running `checklist.py` is mandatory before any commit to the `main` branch.
