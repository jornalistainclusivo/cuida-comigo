---
name: "type-patterns"
description: "Reusable structural patterns for TypeScript and Pydantic data model definitions."
---

# Type Patterns — TypeScript / Zod / OpenAPI 3.1

Reference for the `spec-creator` skill. Contains battle-tested patterns for the Type-first approach. Load only the patterns relevant to the current spec.

---

## Core Principle: Types as Executable Documentation

Every type in a Spec serves two masters simultaneously:

1. **The AI Agent** — reads the type shape and generates correct implementation code
2. **The Runtime** — validated by a paired Zod schema at the system boundary

Always write both together. Never one without the other.

---

## Branded Types — For IDs and Constrained Values

Prevents mixing up IDs of different entity types at compile time. Use for every ID and every string that carries domain meaning.

```typescript
// ── Branded Type Factory ─────────────────────────────────────────────────
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [__brand]: B };

// ── Entity ID Types ────────────────────────────────────────────────────
/** @example "art_01HZXK3N9Y..." — ULID prefixed with entity abbreviation */
type ArticleId = Brand<string, "ArticleId">;
type UserId = Brand<string, "UserId">;
type CategoryId = Brand<string, "CategoryId">;
type OrgId = Brand<string, "OrgId">;

// ── Constrained String Types ───────────────────────────────────────────
/** Non-empty string — prevents empty alt texts, titles, etc. */
type NonEmptyString = Brand<string, "NonEmptyString">;

/** URL-safe slug: lowercase letters, digits, hyphens only */
type Slug = Brand<string, "Slug">;

/** ISO 8601 date-time string (from DB timestamptz) */
type ISODateTime = Brand<string, "ISODateTime">;

/** Semantic version string */
type SemVer = Brand<string, "SemVer">;

// ── Zod Schema for Branded Types ──────────────────────────────────────
import { z } from "zod";

const ArticleIdSchema = z
  .string()
  .regex(/^art_[0-9A-Z]{26}$/, "Invalid ArticleId format")
  .transform((s) => s as ArticleId);

const NonEmptyStringSchema = z
  .string()
  .min(1, "Cannot be empty")
  .transform((s) => s as NonEmptyString);

const SlugSchema = z
  .string()
  .regex(
    /^[a-z0-9-]+$/,
    "Slug must be lowercase letters, digits, and hyphens only",
  )
  .max(255)
  .transform((s) => s as Slug);

// ── Runtime Constructor Helper (avoids type assertion at call sites) ──
const asArticleId = (raw: string): ArticleId => ArticleIdSchema.parse(raw);
```

---

## Domain Entity Interface Pattern

Standard structure for any domain entity in a JINC Spec.

```typescript
import { z } from "zod";

// ── 1. TypeScript Interface (structural contract) ──────────────────────

/**
 * @spec-ref FR-001, FR-002
 * @description Editorial article with full lifecycle support.
 * Immutable fields: id, createdAt, publishedAt (once set).
 * Mutable fields: title, content, status (via state machine transitions only).
 */
interface Article {
  readonly id: ArticleId;
  readonly orgId: OrgId;

  // Identity
  title: NonEmptyString;
  slug: Slug;

  // Content
  content: string; // HTML string; max 200_000 chars
  excerpt: string | null; // Auto-generated if null; max 500 chars
  images: ArticleImage[]; // Alt text required on all before publish

  // Classification
  categoryId: CategoryId | null;
  tags: NonEmptyString[]; // Max 10 tags

  // Lifecycle
  status: ArticleStatus; // Controlled via ArticleLifecycleMachine
  authorId: UserId;
  reviewerId: UserId | null; // Set on SUBMIT_FOR_REVIEW

  // Timestamps (all UTC, from DB timestamptz)
  readonly createdAt: ISODateTime;
  updatedAt: ISODateTime;
  publishedAt: ISODateTime | null; // Immutable once set — see BR-PUB-003
  archivedAt: ISODateTime | null;

  // Accessibility (JINC requirement)
  altTexts: Record<string, NonEmptyString>; // key: image URL, value: alt text
  audioDescription: string | null; // Long-form audio description for complex images
}

// ── 2. Discriminated Union for Status ─────────────────────────────────
// Prefer discriminated unions over optional fields for per-state shapes

type ArticleStatus = "draft" | "in_review" | "published" | "archived";

// When different states need different fields, use a discriminated union:
type ArticleByStatus =
  | { status: "draft"; publishedAt: null; archivedAt: null; reviewerId: null }
  | {
      status: "in_review";
      publishedAt: null;
      archivedAt: null;
      reviewerId: UserId;
    }
  | { status: "published"; publishedAt: ISODateTime; archivedAt: null }
  | { status: "archived"; publishedAt: ISODateTime; archivedAt: ISODateTime };

// ── 3. Zod Runtime Schema ──────────────────────────────────────────────

const ArticleImageSchema = z.object({
  url: z.string().url(),
  altText: NonEmptyStringSchema.nullable(),
  caption: z.string().max(300).nullable(),
  width: z.number().int().positive().nullable(),
  height: z.number().int().positive().nullable(),
});

const ArticleSchema = z.object({
  id: ArticleIdSchema,
  orgId: z.string().transform((s) => s as OrgId),

  title: NonEmptyStringSchema,
  slug: SlugSchema,
  content: z.string().max(200_000),
  excerpt: z.string().max(500).nullable(),
  images: z.array(ArticleImageSchema),

  categoryId: z.string().nullable(),
  tags: z.array(NonEmptyStringSchema).max(10),

  status: z.enum(["draft", "in_review", "published", "archived"]),
  authorId: z.string().transform((s) => s as UserId),
  reviewerId: z
    .string()
    .nullable()
    .transform((s) => (s == null ? null : (s as UserId))),

  createdAt: z
    .string()
    .datetime()
    .transform((s) => s as ISODateTime),
  updatedAt: z
    .string()
    .datetime()
    .transform((s) => s as ISODateTime),
  publishedAt: z
    .string()
    .datetime()
    .nullable()
    .transform((s) => (s == null ? null : (s as ISODateTime))),
  archivedAt: z
    .string()
    .datetime()
    .nullable()
    .transform((s) => (s == null ? null : (s as ISODateTime))),

  altTexts: z.record(z.string().url(), NonEmptyStringSchema),
  audioDescription: z.string().nullable(),
});

// ── 4. Inferred Type (use this in runtime code, not the interface) ─────
type ArticleRuntime = z.infer<typeof ArticleSchema>;

// ── 5. Request/Response Types ──────────────────────────────────────────

const CreateArticleRequestSchema = z.object({
  title: NonEmptyStringSchema,
  content: z.string().max(200_000).optional().default(""),
  categoryId: z.string().nullable().optional(),
  tags: z.array(NonEmptyStringSchema).max(10).optional().default([]),
});

const ArticleSummarySchema = z.object({
  id: ArticleIdSchema,
  title: NonEmptyStringSchema,
  slug: SlugSchema,
  status: z.enum(["draft", "in_review", "published", "archived"]),
  authorId: z.string(),
  publishedAt: z.string().datetime().nullable(),
  updatedAt: z.string().datetime(),
});
```

---

## API Request/Response Schemas — OpenAPI 3.1 Components

Inline OpenAPI fragments to be consolidated into `spec.openapi.yaml`.

```yaml
# ── Reusable Schemas ─────────────────────────────────────────────────────
components:
  schemas:
    # Branded ID types
    ArticleId:
      type: string
      pattern: "^art_[0-9A-Z]{26}$"
      example: "art_01HZXK3N9Y2B4C5D6E7F8G9H0"
      description: "ULID prefixed with entity abbreviation. Immutable after creation."

    NonEmptyString:
      type: string
      minLength: 1

    Slug:
      type: string
      pattern: "^[a-z0-9-]+$"
      maxLength: 255
      example: "inclusive-journalism-guide-2024"

    ISODateTime:
      type: string
      format: date-time
      example: "2024-11-15T18:30:00.000Z"

    # Domain entity — Summary (list responses)
    ArticleSummary:
      type: object
      required: [id, title, slug, status, authorId, updatedAt]
      properties:
        id:
          $ref: "#/components/schemas/ArticleId"
        title:
          $ref: "#/components/schemas/NonEmptyString"
        slug:
          $ref: "#/components/schemas/Slug"
        status:
          type: string
          enum: [draft, in_review, published, archived]
        authorId:
          type: string
        publishedAt:
          $ref: "#/components/schemas/ISODateTime"
          nullable: true
        updatedAt:
          $ref: "#/components/schemas/ISODateTime"

    # Standard error envelope
    ApiError:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
          example: "E_ACCESSIBILITY_REQUIRED"
        message:
          type: string
          example: "Alt text missing on 2 image(s)."
        fields:
          type: array
          items:
            type: string
          description: "Dot-path references to invalid fields (for validation errors)"
          example: ["content.images[0].altText"]

    # Pagination meta (all list responses)
    PaginationMeta:
      type: object
      required: [total, page, perPage]
      properties:
        total:
          type: integer
          example: 247
        page:
          type: integer
          minimum: 1
          example: 1
        perPage:
          type: integer
          minimum: 1
          maximum: 100
          example: 20
        nextCursor:
          type: string
          nullable: true
          description: "Cursor for keyset pagination (preferred over offset for large datasets)"

    # Wrapped response envelopes
    ArticleSummaryListResponse:
      type: object
      required: [data, meta]
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/ArticleSummary"
        meta:
          $ref: "#/components/schemas/PaginationMeta"

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "Supabase JWT via PKCE flow. Expires in 1 hour."
```

---

## Zod Refinements — Domain Constraints

Use `.refine()` for constraints that can't be expressed in base schema.

```typescript
// Accessibility constraint: all images must have alt text before publish
const PublishableArticleSchema = ArticleSchema.refine(
  (article) =>
    article.images.every((img) => img.altText !== null && img.altText !== ""),
  {
    message:
      "All images must have non-empty alt text before the article can be published.",
    path: ["images"],
  },
);

// Slug uniqueness is checked at the DB level, but format validated here
const SlugAvailabilityRequestSchema = z.object({
  slug: SlugSchema,
  excludeId: ArticleIdSchema.optional(), // For update scenarios
});

// Bulk operation with size limit
const BulkArchiveRequestSchema = z.object({
  articleIds: z
    .array(ArticleIdSchema)
    .min(1, "At least one article ID required")
    .max(100, "Cannot bulk archive more than 100 articles at once"),
  reason: z.string().max(500).optional(),
});

// Conditional schema — different validation based on status
const ArticleUpdateSchema = z
  .discriminatedUnion("status", [
    z.object({
      status: z.literal("in_review"),
      reviewerId: z
        .string()
        .min(1, "Reviewer ID required when submitting for review"),
    }),
    z.object({
      status: z.literal("draft"),
      reviewerId: z.string().nullable().optional(),
    }),
  ])
  .and(
    z.object({
      title: NonEmptyStringSchema.optional(),
      content: z.string().max(200_000).optional(),
      tags: z.array(NonEmptyStringSchema).max(10).optional(),
    }),
  );
```

---

## Event Schema — AsyncAPI Pattern

For event-driven sections of the Spec (use when SDD specifies an event bus).

```typescript
// ── Domain Events ───────────────────────────────────────────────────────

/**
 * @spec-ref FR-008 — System must emit events on article lifecycle changes
 * @channel jinc.editorial
 */

interface ArticlePublishedEvent {
  type: "article.published";
  version: "1.0";
  id: string; // Event UUID (for deduplication)
  timestamp: ISODateTime;
  payload: {
    articleId: ArticleId;
    orgId: OrgId;
    authorId: UserId;
    slug: Slug;
    publishedAt: ISODateTime;
    categoryId: CategoryId | null;
    tags: NonEmptyString[];
  };
  metadata: {
    traceId: string; // OpenTelemetry trace propagation
    source: "cms-api";
  };
}

interface ArticleArchivedEvent {
  type: "article.archived";
  version: "1.0";
  id: string;
  timestamp: ISODateTime;
  payload: {
    articleId: ArticleId;
    orgId: OrgId;
    archivedAt: ISODateTime;
    archivedBy: UserId;
    reason: string | null;
  };
  metadata: {
    traceId: string;
    source: "cms-api";
  };
}

// Discriminated union for all editorial events
type EditorialEvent = ArticlePublishedEvent | ArticleArchivedEvent;

// AsyncAPI 2.x channel definition fragment
const asyncApiFragment = `
channels:
  jinc.editorial:
    subscribe:
      summary: Receive editorial lifecycle events
      message:
        oneOf:
          - $ref: '#/components/messages/ArticlePublished'
          - $ref: '#/components/messages/ArticleArchived'
`;
```

---

## Utility Types — Common Spec Helpers

```typescript
// ── Spec Utility Types (reusable across specs) ─────────────────────────

/** Makes specified keys required and non-nullable */
type Require<T, K extends keyof T> = T & { [P in K]-?: NonNullable<T[P]> };

/** Makes all nested properties readonly (for immutable domain objects) */
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

/** Pagination params for list endpoints */
interface PaginationParams {
  page?: number; // Default: 1, Min: 1
  perPage?: number; // Default: 20, Min: 1, Max: 100
  cursor?: string; // Keyset cursor (exclusive with page/perPage)
}

/** Standard paginated response envelope */
interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    perPage: number;
    nextCursor: string | null;
  };
}

/** Standard API error (matches ApiError OpenAPI schema) */
interface ApiError {
  code: string;
  message: string;
  fields?: string[]; // Dot-path references for validation errors
}

/** Result type for service layer (avoids throw/catch at business logic level) */
type Result<T, E = ApiError> = { ok: true; value: T } | { ok: false; error: E };

// Constructor helpers
const ok = <T>(value: T): Result<T> => ({ ok: true, value });
const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
```
