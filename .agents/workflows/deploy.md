---
description: Protocol for committing, validating, and deploying repository changes, ensuring compliance with WCAG 2.2, SDD Pydantic, and CI/CD integrity.
---

---

name: "deploy-workflow"
description: "Standard protocol for committing, validating, and deploying repository changes via SDD Gatekeeper."

---

# /deploy - Workflow Deployment

$ARGUMENTS

---

## Deploy & Git Flow Protocol

This workflow defines the "exit" rules for code and manifests. As an Orchestrator, you must follow this protocol to ensure that changes do not break the validation infrastructure.

### 1. Pre-flight Verification (Integrity Checklist)

Before performing any commit, verify if the changes meet the governance requirements:

- [ ] **YAML Sanitization:** Are all `description` keys in the frontmatter of `.md` files enclosed in double quotes `"..."`?
- [ ] **Pydantic Validation:** Has the `.agents/scripts/checklist.py` script been executed locally without errors?
- [ ] **Accessibility:** For any UI changes, have WCAG 2.2 AAA standards been respected?
- [ ] **Formatting:** Has the `npm run format` command been executed to align style via Prettier?

### 2. Branching Protocol

Never commit directly to the `main` branch for complex tasks.

1. **Feature Branch Creation:** `git checkout -b feature/[task-name]`
2. **Isolation:** Ensure the branch contains only files related to the specific task.

### 3. Commit Execution (The Gating Mechanism)

The repository uses **Husky** and **lint-staged**. When you trigger a commit, the local gating mechanism will be activated automatically.

**Command:**

```bash
git add .
git commit -m "[type]: clear description of what was changed"
```

**Acceptable Commit Types:**

- `feat`: New skill or agent.
- `fix`: Error correction in script or manifest.
- `docs`: Changes in README or ARCHITECTURE.
- `chore`: Update of dependencies or CI/CD.
- `refactor`: Logic improvement without changing functionality.

### 4. Commit Error Management

If the commit fails (❌ icon in terminal):

1. **Read Pydantic Error:** Identify which file and which key broke the contract.
2. **Fix and Re-stage:** Apply the fix, run `git add .`, and attempt the commit again.
3. **Do Not Ignore the Gatekeeper:** If Husky blocks the commit, the code is structurally incorrect.

### 5. Synchronization and Remote Verification

After a successful local commit:

1. **Push:** `git push origin [branch-name]`
2. **GitHub Actions:** Monitor the 'Actions' tab on GitHub.
3. **Merge:** Only perform the merge to `main` if the `validate-architecture` job returns success (✅).

---

**Note for the Orchestrator:** If the user asks to "save everything" or "deploy," assume this workflow as your standard execution guide.
