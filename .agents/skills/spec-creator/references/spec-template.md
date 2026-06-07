---
name: "spec-template"
description: "Standardized blueprint for creating high-fidelity SDD technical specifications."
---

# Spec Template — Full Section Examples

Reference file for the `spec-creator` skill. Load only the sections you need.

---

## API Contract Section — Full Format

### REST Endpoint Specification

````markdown
### Endpoint: Publish Article

#### 🤖 AI-Ready Layer

**OpenAPI 3.1 Fragment**

```yaml
/articles/{id}/publish:
  post:
    operationId: publishArticle
    summary: Publish a drafted article after accessibility validation
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        required: true
        schema:
          $ref: "#/components/schemas/ArticleId"
    requestBody:
      required: false
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/PublishArticleRequest"
    responses:
      "200":
        description: Article published successfully
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ArticlePublishedResponse"
      "400":
        description: Validation failed
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ApiError"
            examples:
              missing_alt_text:
                value:
                  code: E_ACCESSIBILITY_REQUIRED
                  message: "Alt text missing on 2 image(s). Provide alt text before publishing."
                  fields:
                    ["content.images[0].altText", "content.images[2].altText"]
      "403":
        description: Insufficient role
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ApiError"
            examples:
              contributor_blocked:
                value:
                  code: E_AUTH_FORBIDDEN
                  message: "Contributors cannot publish directly. Submit for review."
      "409":
        description: Article already published or archived
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ApiError"
```
````

**Concrete I/O Examples**

```
// ✅ Success — Editor publishes article with valid alt texts
Request:
  POST /api/v1/articles/art_01HZXK3N9Y2B4C5D6E7F8G9H0/publish
  Authorization: Bearer <editor-jwt>
  Body: {} // no override needed

Response 200:
  {
    "data": {
      "id": "art_01HZXK3N9Y2B4C5D6E7F8G9H0",
      "status": "published",
      "slug": "inclusive-journalism-guide-2024",
      "publishedAt": "2024-11-15T18:30:00.000Z"
    }
  }

// ❌ Failure — Missing alt text blocks publish
Response 400:
  {
    "error": {
      "code": "E_ACCESSIBILITY_REQUIRED",
      "message": "Alt text missing on 2 image(s). Provide alt text before publishing.",
      "fields": ["content.images[0].altText", "content.images[2].altText"]
    }
  }
```

#### 🔧 Implementation Layer

**Algorithm:**

1. Resolve `articleId` from path parameter. If not found → 404
2. Assert `article.status` is `draft` or `review`. If `published` or `archived` → 409 E_CONFLICT
3. Assert caller has role `editor` or `admin`. If `contributor` → 403 E_AUTH_FORBIDDEN
4. Run accessibility check: scan `article.content` for `<img>` tags without `altText`. Collect violations.
5. If violations.length > 0 → 400 E_ACCESSIBILITY_REQUIRED with `fields` array of missing paths
6. All checks pass → set `article.status = "published"`, `article.publishedAt = NOW()`
7. Emit event `article.published` on `jinc.editorial` channel
8. Return 200 with updated article summary

**Preconditions:**

- Article exists in DB and belongs to the caller's organization
- JWT is valid and not expired
- Request passes rate limit: 10 publish operations per minute per user

**Postconditions:**

- `article.status === "published"` in DB
- `article.publishedAt` is set and immutable after this point
- Event `article.published` is in the event queue (at-least-once delivery)

#### 🔗 Traceability Layer

- Covers: FR-002 (alt-text required), FR-005 (role-based publishing)
- ADR-003 (SDD): Supabase RLS enforces org-level access at DB level
- Rationale for 409 over 400 on status conflict: Idempotency concern — client may retry; 409 signals "state mismatch" not "bad input"

````

---

## State Machine Section — XState Format

```markdown
### State Machine: Article Lifecycle

#### 🤖 AI-Ready Layer

```typescript
import { createMachine, assign } from 'xstate';

/** @spec-ref FR-009, FR-010 */
const articleLifecycleMachine = createMachine({
  id: 'articleLifecycle',
  initial: 'draft',
  context: {
    reviewerId: null as string | null,
    publishedAt: null as Date | null,
    rejectionReason: null as string | null,
  },
  states: {
    draft: {
      on: {
        SUBMIT_FOR_REVIEW: {
          target: 'in_review',
          guard: 'hasRequiredContent',
          actions: assign({ reviewerId: ({ event }) => event.reviewerId }),
        },
        // Contributors and editors can submit; admins can bypass directly
        PUBLISH_DIRECTLY: {
          target: 'published',
          guard: 'isEditorOrAdmin',
          actions: assign({ publishedAt: () => new Date() }),
        },
      },
    },
    in_review: {
      on: {
        APPROVE: {
          target: 'published',
          guard: 'isReviewerOrAdmin',
          actions: assign({ publishedAt: () => new Date() }),
        },
        REJECT: {
          target: 'draft',
          guard: 'isReviewerOrAdmin',
          actions: assign({ rejectionReason: ({ event }) => event.reason }),
        },
      },
    },
    published: {
      on: {
        ARCHIVE: {
          target: 'archived',
          guard: 'isEditorOrAdmin',
        },
        // Published articles can be unpublished back to draft for correction
        UNPUBLISH: {
          target: 'draft',
          guard: 'isAdmin',
        },
      },
    },
    archived: {
      type: 'final', // Terminal state — no transitions out (use restore flow for reversal)
    },
  },
});
````

**State Transition Table**

| From        | Event               | Guard                | To          | Side Effect                    |
| ----------- | ------------------- | -------------------- | ----------- | ------------------------------ |
| `draft`     | `SUBMIT_FOR_REVIEW` | `hasRequiredContent` | `in_review` | Notify reviewer                |
| `draft`     | `PUBLISH_DIRECTLY`  | `isEditorOrAdmin`    | `published` | Emit `article.published` event |
| `in_review` | `APPROVE`           | `isReviewerOrAdmin`  | `published` | Emit `article.published` event |
| `in_review` | `REJECT`            | `isReviewerOrAdmin`  | `draft`     | Notify author with reason      |
| `published` | `ARCHIVE`           | `isEditorOrAdmin`    | `archived`  | Emit `article.archived` event  |
| `published` | `UNPUBLISH`         | `isAdmin`            | `draft`     | Audit log entry required       |
| `archived`  | —                   | —                    | —           | Terminal. No exits.            |

#### 🔧 Implementation Layer

**Guard Implementations:**

```typescript
const guards = {
  hasRequiredContent: ({ context, event }) =>
    event.article.title.length > 0 &&
    event.article.content.length >= 100 &&
    event.article.images.every(
      (img) => img.altText !== null && img.altText !== "",
    ),

  isEditorOrAdmin: ({ context, event }) =>
    ["editor", "admin"].includes(event.callerRole),

  isReviewerOrAdmin: ({ context, event }) =>
    event.callerRole === "admin" ||
    (event.callerRole === "editor" && event.callerId === context.reviewerId),

  isAdmin: ({ context, event }) => event.callerRole === "admin",
};
```

**Invariants (never violated regardless of transition):**

- `publishedAt` is immutable once set (only set once on transition → `published`)
- `archived` articles cannot be directly edited — clone and create new draft instead
- `rejectionReason` is always displayed to the original author; never silently discarded

#### 🔗 Traceability Layer

- Covers: FR-009 (workflow states), FR-010 (role-based transitions), FR-011 (audit trail)
- ADR-004 (SDD): Status stored as `TEXT` with CHECK constraint in Postgres, not enum (allows migration without schema change)

````

---

## Business Rules — Full Examples

```markdown
### Business Rules: Article Publishing

BR-PUB-001: Alt Text Required Before Publish
  Precondition:  Article status is `draft` or `in_review`
  Input:         PUBLISH or APPROVE transition event
  Invariant:     No published article may contain an image without altText
  Output:        Publication proceeds; article.status → "published"
  Violation:     E_ACCESSIBILITY_REQUIRED — "Alt text missing on N image(s). Add alt text to: [field paths]"
  I/O Example:
    Input:    article.content contains <img src="photo.jpg" altText="">
    Output:   Error E_ACCESSIBILITY_REQUIRED, fields: ["content.images[0].altText"]

BR-PUB-002: Contributor Cannot Publish Directly
  Precondition:  Caller has role "contributor"
  Input:         PUBLISH_DIRECTLY event
  Invariant:     Contributors always route through review workflow
  Output:        N/A — blocked
  Violation:     E_AUTH_FORBIDDEN — "Contributors cannot publish directly. Use 'Submit for Review'."
  I/O Example:
    Input:    { callerId: "user_123", callerRole: "contributor", articleId: "art_456" }
    Output:   Error E_AUTH_FORBIDDEN

BR-PUB-003: Published Date Is Immutable
  Precondition:  article.publishedAt IS NOT NULL
  Input:         Any update attempt on publishedAt field
  Invariant:     publishedAt never changes after first publication
  Output:        N/A — silently ignored; field not updated
  Violation:     N/A — silently rejected (no error; callers should not attempt override)
  I/O Example:
    Input:    PATCH /articles/art_456 { publishedAt: "2020-01-01" }
    Output:   200 OK — but publishedAt unchanged in DB
````

---

## Error Code Registry (Spec-Level)

Define all error codes the feature introduces. Reference in Business Rules and API Contract.

```markdown
### Error Codes — [Feature Name]

| Code                       | HTTP Status | Trigger Condition                        | User-Facing Message                                  |
| -------------------------- | ----------- | ---------------------------------------- | ---------------------------------------------------- |
| `E_ACCESSIBILITY_REQUIRED` | 400         | Alt text missing on publish              | "Alt text required on all images before publishing." |
| `E_AUTH_FORBIDDEN`         | 403         | Role insufficient for action             | "Your role does not permit this action."             |
| `E_AUTH_REQUIRED`          | 401         | No valid JWT                             | "Authentication required."                           |
| `E_NOT_FOUND`              | 404         | Resource doesn't exist                   | "Resource not found."                                |
| `E_CONFLICT`               | 409         | State mismatch (e.g., already published) | "Cannot perform this action in the current state."   |
| `E_VALIDATION_FAILED`      | 422         | Input schema validation failure          | "Input validation failed. See fields for details."   |
| `E_RATE_LIMITED`           | 429         | Exceeded rate limit                      | "Too many requests. Try again in {retryAfter}s."     |
```
