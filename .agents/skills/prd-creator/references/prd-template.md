---
name: "prd-template"
description: "Reference for the PRD template."
---

# PRD Template — Full 10-Section Structure

Reference for `prd-creator`. Load when drafting the full PRD after Phase 2 (Frame) is complete.

---

## How to Use This Template

- Replace `[placeholders]` with real content
- Mark inferred content with `[🟡 Assumed — validate with: source]`
- Mark blocking gaps with `[🔴 OPEN — blocks SDD section: X]`
- Delete sections not applicable to the project type (document why with one line)
- Accessibility Requirements section is MANDATORY for all user-facing products

---

```markdown
---
jinc-prd-version: 1.0.0
project-name: [Project or Product Name]
feature-name: [Specific feature or epic scope]
status: draft
related-branch: docs/prd-[feature-name]
product-context: [mobile|web|backend|fullstack|internal]
created-at: [YYYY-MM-DD]
last-updated: [YYYY-MM-DD]
authors: [Name]
---

# [Product Name] — Product Requirements Document

## 1. Executive Summary

| Field                        | Value                                                             |
| ---------------------------- | ----------------------------------------------------------------- |
| **Vision**                   | [One sentence: what does the world look like when this succeeds?] |
| **Target Users**             | [Primary persona(s)]                                              |
| **Core Problem**             | [What's broken today — in one sentence]                           |
| **Proposed Solution**        | [What the product does — no implementation details]               |
| **Strategic Alignment**      | [Which JINC OKR or mission pillar this serves]                    |
| **Key Differentiator**       | [Why JINC's version of this is uniquely valuable]                 |
| **Success Metric (Primary)** | [The one number that proves this worked]                          |
| **Timeline Target**          | [When MVP should be in users' hands]                              |
| **Resource Estimate**        | [🟡 Assumed — ballpark: N engineers × N weeks]                    |

---

## 2. Problem and Opportunity

### Problem Definition

[2-4 paragraphs. Structure: What is happening today? Who is affected and how many? What is the cost of inaction (in time, money, or mission impact)? What has been tried before and why it failed?]

**Quantified Impact (current state):**

- [Metric 1]: [Current baseline] → [User experience consequence]
- [Metric 2]: [Current baseline] → [Business consequence]

> Example:
> Journalists with visual impairments currently require a sighted assistant to upload images with correct alt texts, adding 45-90 minutes per article and introducing a dependency that breaks their editorial independence.

### Root Cause Analysis

[Why does this problem exist? Not symptoms — the actual root cause. Use the 5 Whys if helpful.]

1. **Why 1:** [Symptom → underlying cause]
2. **Why 2:** [Cause → deeper cause]
3. **Root cause:** [The actual problem to solve]

### Opportunity

| Dimension                 | Assessment                                                    |
| ------------------------- | ------------------------------------------------------------- |
| **Market size**           | [Number of affected users / potential users]                  |
| **Revenue opportunity**   | [🟡 Assumed if estimating]                                    |
| **Mission alignment**     | [How this advances inclusive journalism]                      |
| **Competitive landscape** | [Who else is solving this? How is JINC's approach different?] |
| **Window of opportunity** | [Why now? What changes if we wait 6 months?]                  |

---

## 3. User Requirements

### Primary Personas

**Persona 1: [Name / Role]**

- **Context:** [Situation in which they use the product]
- **Goals:** [What they're trying to achieve]
- **Pain points:** [What frustrates them today]
- **Tech literacy:** [Low / Medium / High]
- **Disability/accessibility context:** [If applicable — screen reader, motor limitations, cognitive load, etc.]
- **Quote (real or representative):** _"[Voice of the user]"_

**Persona 2: [Name / Role]**

- [Same structure]

### Jobs to be Done

When [context/trigger], I want to [action/motivation], so I can [outcome/benefit].

- **JTBD-001:** When I finish writing an article, I want to add descriptive alt text to all images in one step, so I can publish without needing help from a sighted colleague.
- **JTBD-002:** When I review a draft for publication, I want the system to warn me about incomplete accessibility requirements, so I can prevent non-compliant content from going live.
- [Add 3-7 JTBDs — the most important ones]

### User Journey Map
```

[Persona: Name] — Flow: [Core Use Case]

Current (Painful) Journey:

1. [Step 1] → 😤 Pain: [what's wrong]
2. [Step 2] → ⏱️ Friction: [what slows them down]
3. [Step 3] → 🔴 Blocker: [what stops them entirely]

Future (With Product) Journey:

1. [Step 1] → ✅ [Improved experience]
2. [Step 2] → ✅ [Time/effort saved]
3. [Step 3] → ✅ [New outcome achieved]

```

### User Stories

**Epic: [Epic Name]**

**US-001: [Short title]**
- As a **[persona]**
- I want to **[action]**
- So that **[outcome]**
- **Acceptance Criteria:**
  - [ ] Given [precondition], When [action], Then [verifiable result]
  - [ ] Given [edge condition], When [action], Then [graceful result]
  - [ ] Given [error condition], When [action], Then [clear error with recovery path]

**US-002: [Short title]**
- [Same structure]

[Add 3-10 stories — prioritized by JTBD importance]

---

## 4. Functional Requirements

### Must-Have (MVP — P0)

| ID | Requirement | User Story | Notes |
|----|-------------|------------|-------|
| FR-001 | [System shall...] — use declarative language, no implementation | US-001 | [Constraint or rationale] |
| FR-002 | [System shall...] | US-002 | |

**Rule:** Never write implementation in requirements.
- ❌ "System shall display a modal with a textarea field"
- ✅ "System shall allow users to input alt text for each image before publishing"

### Should-Have (V1 — P1)

| ID | Requirement | Rationale for deferral |
|----|-------------|------------------------|
| FR-010 | [Requirement] | [Why this can wait for V1 without blocking MVP value] |

### Nice-to-Have (Backlog — P2)

| ID | Requirement | Trigger for promotion |
|----|-------------|----------------------|
| FR-020 | [Requirement] | [What signal would move this to P1] |

### Explicit Non-Goals

Document what this product deliberately does NOT do. This prevents scope creep and manages stakeholder expectations.

- **Not in scope:** [Feature or behavior] — because [reason]. To be addressed by [alternative or future initiative].
- **Not in scope:** [Feature or behavior] — because [reason].
- [Add at least 2 non-goals]

### Feature Prioritization

| Feature | Business Value | User Impact | Effort | Priority | Phase |
|---------|---------------|-------------|--------|----------|-------|
| [Feature] | High/Med/Low | High/Med/Low | XS/S/M/L/XL | P0/P1/P2 | MVP/V1/Scale |

---

## 5. Accessibility Requirements

**⚠️ MANDATORY for all user-facing products — JINC standard**

| Requirement | WCAG Criterion | Target Level | Notes |
|-------------|----------------|-------------|-------|
| Keyboard navigation | 2.1.1 | AAA | Full Tab/Shift+Tab with logical order |
| Focus indicator visible | 2.4.7 | AA | `focus-visible` ring on all interactive elements |
| Text contrast ratio | 1.4.3 | AAA | Minimum 7:1 (not 4.5:1) |
| Images have alt text | 1.1.1 | A | Required before publishing; product must enforce |
| Error messages are descriptive | 3.3.1 | A | Not just "Error" — must tell user what to do |
| Screen reader compatibility | 4.1.3 | AA | Test with NVDA (Windows) + VoiceOver (iOS/macOS) |
| Content reflow at 400% zoom | 1.4.10 | AA | No horizontal scroll on single-column content |
| No auto-playing media | 1.4.2 | A | No audio/video starts without explicit user action |

**Specific product accessibility concerns:**
[List the components or flows in this product that have non-obvious accessibility requirements. E.g., "The image upload flow must announce upload progress to screen readers."]

---

## 6. User Experience Requirements

### Design Principles (for this product)

[3-5 principles that specifically guide this product's UX — not generic "simple and clean" but specific to this user context]

1. **Independence over assistance:** Every action must be completable without relying on another person.
2. **[Principle 2]:** [Specific to this product]
3. **[Principle 3]:** [Specific to this product]

### JINC Design System Constraints

- Color: Neutral palette only (`neutral-50` to `neutral-900`). No purple/violet.
- Content width: Max `70ch` for readable text.
- Typography: Serif for editorial content, Sans for UI elements.
- Motion: All animations must respect `prefers-reduced-motion`.

### Interface Requirements

[What must the interface support — without specifying how to implement it]

- "Users must be able to complete the primary flow on mobile (iOS Safari, Android Chrome)"
- "Interface must adapt to 150% browser zoom without breaking core functionality"
- [Add 3-5 interface-level requirements]

---

## 7. Non-Functional Requirements

### Performance

| Metric | Requirement | Notes |
|--------|-------------|-------|
| Page load (First Contentful Paint) | < 1.8s | LCP < 2.5s (Core Web Vitals) |
| API response time (p95) | < 200ms | Document exceptions explicitly |
| Concurrent users (MVP) | [N users] | 🟡 Assumed — validate with engineering |
| Availability | 99.5% uptime | Exclude planned maintenance |

### Security

- Authentication: Supabase Auth (PKCE) — no implicit flows
- Authorization: Role-based; document roles and permissions per action
- Data handling: No PII in logs, no secrets in code
- Compliance: [LGPD / GDPR applicability — note data residency if relevant]

### Reliability

- Error handling: All user-visible errors must have a recovery path (not just "an error occurred")
- Data persistence: [Define acceptable data loss window — e.g., "No loss of user input older than 30 seconds"]
- Graceful degradation: [What happens when a dependency is unavailable?]

### Scalability

| Dimension | MVP Baseline | 12-Month Target |
|-----------|-------------|-----------------|
| Active users | [N] | [N] |
| Content volume | [N articles/day] | [N articles/day] |
| Storage growth | [GB/month] | [GB/month] |

---

## 8. Success Metrics and Analytics

### Primary KPIs (North Star Metrics)

| Metric | Baseline | MVP Target | V1 Target | Measurement Method |
|--------|----------|------------|-----------|-------------------|
| [Primary metric] | [Current] | [Goal] | [Goal] | [How it's tracked] |

### Secondary KPIs

| Metric | Baseline | Target | Notes |
|--------|----------|--------|-------|
| [Secondary metric] | | | |

### Analytics Implementation

[What events must be tracked? What properties are needed on each event?]

- `article.publishing_started` — properties: `user_role`, `article_id`, `has_images`
- `article.published` — properties: `user_role`, `article_id`, `time_to_publish_ms`, `accessibility_auto_filled`
- `accessibility.alt_text_added` — properties: `method: ['manual', 'ai_generated']`, `article_id`

### Guardrail Metrics (Do Not Worsen)

| Metric | Current Baseline | Alert Threshold |
|--------|-----------------|-----------------|
| [Metric we must not break] | [Value] | [% or absolute change that triggers concern] |

---

## 9. Implementation Considerations

**Note:** This section informs SDD architecture decisions — not implementation decisions. Do NOT specify how to build; specify what constraints the engineering team must be aware of.

### Technical Context

- **Existing stack:** [What already exists that this must integrate with]
- **Integration points:** [External systems, APIs, or services this product depends on]
- **Data requirements:** [Key entities, relationships, data volume hints]
- **Migration needs:** [Is there existing data or behavior to migrate?]
- **Platform targets:** [Web only / Mobile / Both / API-only]

### Constraints

- **Compliance:** [LGPD, WCAG, GDPR, editorial policy constraints]
- **Performance:** [Specific limits the architecture must respect — see Non-Functional Requirements]
- **Availability:** [Hosting, deployment, geographic requirements]
- **Security:** [Auth requirements, data handling constraints]

### Open Technical Questions (for SDD)

These are questions this PRD cannot answer — they must be resolved in the SDD:

- 🟡 [Technical question about architecture that product can't predetermine]
- 🟡 [Another open question for engineering]

---

## 10. Risk Assessment

### Risk Register

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|-----------|-------|
| R-001 | [Risk description] | High/Med/Low | High/Med/Low | [Specific mitigation action] | [Role] |
| R-002 | [Research/assumption not validated] | | | [Validated by: user research, prototype, etc.] | |

### Assumptions and Validations Needed

| Assumption | How to Validate | Deadline | Status |
|-----------|-----------------|----------|--------|
| [🟡 Assumed item from Frame phase] | [Interview N users / A-B test / desk research] | [Date] | Pending |

---

## Downstream Pipeline

This PRD is the input for:

- **SDD (Architecture Design):** Use `sdd-creator`. Priority sections to process: Technical Context, Non-Functional Requirements, Data Requirements.
- **Spec (Technical Specification):** Use `spec-creator`. Priority sections to process: Functional Requirements, User Stories (Acceptance Criteria), Business Rules implied by FR constraints.

| Status | Value |
|--------|-------|
| PRD Status | draft |
| Ready for SDD? | 🟡 Pending validation of: [items] |
| Stakeholder sign-off | 🔴 Required before SDD starts |
```
