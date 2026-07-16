# OpenClaw myconversation Media (Send File) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable the OpenClaw myconversation channel plugin to send and receive images + document files in staff group chat (no video), using myEdge multipart upload and local-temp inbound downloads.

**Architecture:** Add a focused `src/media/` layer (classify, limits, upload, download, context, outbound orchestration). Wire inbound `dispatch.ts` to download attachments into temp paths and set `MediaPaths`; wire outbound `deliver` + `attachedResults.sendMedia` to upload then `SendChatGroupMessage` with `images[]`/`files[]`. No Go backend changes.

**Tech Stack:** TypeScript, Vitest, `@connectrpc/connect` + `@connectrpc/connect-node`, `@genjutsu/myconversation-connect`, `@genjutsu/myedge-connect` `^1.1.0`, OpenClaw plugin-sdk (`MediaPaths`, `sendMedia`, `mediaUrls`)

**Spec:** `docs/superpowers/specs/2026-07-09-openclaw-myconversation-media-design.md`

---

## File map

| File | Responsibility |
|------|----------------|
| `src/media/limits.ts` | `MAX_ATTACHMENTS=5`, `MAX_FILE_BYTES=20MB`, `selectInboundAttachments`, `assertOutboundAttachmentLimits` |
| `src/media/classify.ts` | MIME/path → `"image" \| "document" \| "video"`; bucket into `images`/`files` |
| `src/media/paths.ts` | Normalize upload paths; detect protected `api/v1/upload/...`; resolve fetch URLs |
| `src/media/upload.ts` | myEdge multipart upload (Node Buffer); return object keys |
| `src/media/download.ts` | Auth/static fetch → temp dir; cleanup helper |
| `src/media/context.ts` | Append `[Ảnh:]` / `[Tệp:]` lines; build inbound `MediaPaths` |
| `src/media/outbound.ts` | Resolve agent media inputs → upload → `{ images, files }` |
| `src/connect/myedge.ts` | myEdge Connect client factory (same auth as myconversation) |
| `src/config.ts` | Parse `staticUrl`, `mediaTempDir`; export defaults |
| `src/outbound/reply.ts` | File-only chunked send; keep media on first chunk |
| `src/inbound/dispatch.ts` | Download after mention gate; enrich context; deliver media |
| `src/channel.ts` | `media: true`; `attachedResults.sendMedia` |
| `openclaw.plugin.json` | Schema for `staticUrl`, `mediaTempDir` |
| `package.json` | Add `@genjutsu/myedge-connect` |
| `README.md` | Document media behavior + config |

---

### Task 1: Add dependency + config fields

**Files:**
- Modify: `package.json`
- Modify: `src/config.ts`
- Modify: `src/config.test.ts`
- Modify: `openclaw.plugin.json`

- [ ] **Step 1: Add dependency**

```bash
cd /Users/nemo/go/src/gitlab.genjutsu.ai/marketplace/openclaw/myconversation
pnpm add @genjutsu/myedge-connect@^1.1.0
```

Expected: `package.json` lists `"@genjutsu/myedge-connect": "^1.1.0"` (or compatible resolved version).

- [ ] **Step 2: Write failing config tests**

Add to `src/config.test.ts`:

```typescript
it("parses optional staticUrl and mediaTempDir", () => {
  const config = parseMyConversationChannelConfig({
    endpoint: "https://gw.example.com",
    tenantId: "tenant-abc",
    token: "token",
    staticUrl: "https://s.example.com/",
    mediaTempDir: "/tmp/myconv-media",
  });
  expect(config.staticUrl).toBe("https://s.example.com");
  expect(config.mediaTempDir).toBe("/tmp/myconv-media");
});

it("defaults staticUrl and mediaTempDir to undefined", () => {
  const config = parseMyConversationChannelConfig({
    endpoint: "mc:8080",
    tenantId: "tenant-abc",
    token: "token",
  });
  expect(config.staticUrl).toBeUndefined();
  expect(config.mediaTempDir).toBeUndefined();
});
```

- [ ] **Step 3: Run test to verify it fails**

```bash
pnpm test src/config.test.ts
```

Expected: FAIL — `staticUrl` / `mediaTempDir` not on config type / undefined unexpectedly wrong.

- [ ] **Step 4: Implement config parsing**

In `src/config.ts`, extend `MyConversationChannelConfig`:

```typescript
export type MyConversationChannelConfig = {
  endpoint: string;
  tenantId: string;
  token: string;
  userId?: string;
  username?: string;
  activeGroupsPolicy: ActiveGroupsPolicy;
  groups: Record<string, MyConversationGroupConfig>;
  /** Public static host for inbound media read fallback (no trailing slash). */
  staticUrl?: string;
  /** Override root for inbound download temp dirs. */
  mediaTempDir?: string;
};
```

Add helpers and wire into `parseMyConversationChannelConfig`:

```typescript
function parseOptionalUrl(value: unknown, field: string): string | undefined {
  if (value == null) return undefined;
  if (typeof value !== "string") {
    throw new Error(`myconversation: ${field} must be a string`);
  }
  const trimmed = value.trim().replace(/\/+$/, "");
  return trimmed === "" ? undefined : trimmed;
}

function parseOptionalPath(value: unknown, field: string): string | undefined {
  if (value == null) return undefined;
  if (typeof value !== "string") {
    throw new Error(`myconversation: ${field} must be a string`);
  }
  const trimmed = value.trim();
  return trimmed === "" ? undefined : trimmed;
}
```

Return:

```typescript
staticUrl: parseOptionalUrl(input.staticUrl, "staticUrl"),
mediaTempDir: parseOptionalPath(input.mediaTempDir, "mediaTempDir"),
```

Also add properties to `myConversationChannelConfigSchema` and `openclaw.plugin.json` `channelConfigs.myconversation.schema.properties`:

```json
"staticUrl": {
  "type": "string",
  "description": "Optional public static host for inbound media reads (e.g. https://s.example.com)"
},
"mediaTempDir": {
  "type": "string",
  "description": "Optional override for inbound media temp directory root"
}
```

- [ ] **Step 5: Run tests**

```bash
pnpm test src/config.test.ts
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add package.json pnpm-lock.yaml src/config.ts src/config.test.ts openclaw.plugin.json
git commit -m "$(cat <<'EOF'
feat(myconversation): add myedge dep and media config fields

EOF
)"
```

---

### Task 2: `limits` + `classify` (TDD)

**Files:**
- Create: `src/media/limits.ts`
- Create: `src/media/classify.ts`
- Create: `src/media/limits.test.ts`
- Create: `src/media/classify.test.ts`

- [ ] **Step 1: Write failing tests**

`src/media/limits.test.ts`:

```typescript
import { describe, expect, it } from "vitest";
import {
  MAX_ATTACHMENTS,
  MAX_FILE_BYTES,
  selectInboundAttachments,
  assertOutboundAttachmentLimits,
} from "./limits.js";

describe("selectInboundAttachments", () => {
  it("keeps images first then files, capped at MAX_ATTACHMENTS", () => {
    const images = ["i1", "i2", "i3"];
    const files = ["f1", "f2", "f3"];
    const selected = selectInboundAttachments({ images, files });
    expect(MAX_ATTACHMENTS).toBe(5);
    expect(selected).toEqual([
      { kind: "image", path: "i1" },
      { kind: "image", path: "i2" },
      { kind: "image", path: "i3" },
      { kind: "document", path: "f1" },
      { kind: "document", path: "f2" },
    ]);
  });

  it("ignores empty strings", () => {
    expect(
      selectInboundAttachments({ images: ["", "a"], files: ["  "] }),
    ).toEqual([{ kind: "image", path: "a" }]);
  });
});

describe("assertOutboundAttachmentLimits", () => {
  it("throws when more than MAX_ATTACHMENTS", () => {
    expect(() =>
      assertOutboundAttachmentLimits(
        Array.from({ length: 6 }, (_, i) => ({ size: 1, name: `f${i}` })),
      ),
    ).toThrow(/5/);
  });

  it("throws when a file exceeds MAX_FILE_BYTES", () => {
    expect(() =>
      assertOutboundAttachmentLimits([
        { size: MAX_FILE_BYTES + 1, name: "big.pdf" },
      ]),
    ).toThrow(/20/);
  });

  it("allows up to 5 files within size", () => {
    expect(() =>
      assertOutboundAttachmentLimits(
        Array.from({ length: 5 }, (_, i) => ({
          size: MAX_FILE_BYTES,
          name: `f${i}`,
        })),
      ),
    ).not.toThrow();
  });
});
```

`src/media/classify.test.ts`:

```typescript
import { describe, expect, it } from "vitest";
import {
  classifyMediaKind,
  bucketOutboundPaths,
} from "./classify.js";

describe("classifyMediaKind", () => {
  it("classifies image MIME and extensions", () => {
    expect(classifyMediaKind({ contentType: "image/png" })).toBe("image");
    expect(classifyMediaKind({ path: "photo.JPG" })).toBe("image");
  });

  it("classifies video as video", () => {
    expect(classifyMediaKind({ contentType: "video/mp4" })).toBe("video");
    expect(classifyMediaKind({ path: "clip.webm" })).toBe("video");
  });

  it("classifies everything else as document", () => {
    expect(classifyMediaKind({ contentType: "application/pdf" })).toBe(
      "document",
    );
    expect(classifyMediaKind({ path: "notes.txt" })).toBe("document");
    expect(classifyMediaKind({ path: "archive.zip" })).toBe("document");
  });
});

describe("bucketOutboundPaths", () => {
  it("splits images and files and skips videos", () => {
    const result = bucketOutboundPaths([
      { path: "a.png", contentType: "image/png" },
      { path: "b.pdf", contentType: "application/pdf" },
      { path: "c.mp4", contentType: "video/mp4" },
    ]);
    expect(result.images).toEqual(["a.png"]);
    expect(result.files).toEqual(["b.pdf"]);
    expect(result.skippedVideos).toEqual(["c.mp4"]);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pnpm test src/media/limits.test.ts src/media/classify.test.ts
```

Expected: FAIL — modules not found.

- [ ] **Step 3: Implement**

`src/media/limits.ts`:

```typescript
export const MAX_ATTACHMENTS = 5;
export const MAX_FILE_BYTES = 20 * 1024 * 1024;

export type InboundAttachmentRef = {
  kind: "image" | "document";
  path: string;
};

export function selectInboundAttachments(params: {
  images?: string[];
  files?: string[];
}): InboundAttachmentRef[] {
  const out: InboundAttachmentRef[] = [];
  for (const path of params.images ?? []) {
    const trimmed = path.trim();
    if (!trimmed) continue;
    out.push({ kind: "image", path: trimmed });
    if (out.length >= MAX_ATTACHMENTS) return out;
  }
  for (const path of params.files ?? []) {
    const trimmed = path.trim();
    if (!trimmed) continue;
    out.push({ kind: "document", path: trimmed });
    if (out.length >= MAX_ATTACHMENTS) return out;
  }
  return out;
}

export function assertOutboundAttachmentLimits(
  items: Array<{ size: number; name: string }>,
): void {
  if (items.length > MAX_ATTACHMENTS) {
    throw new Error(
      `myconversation: at most ${MAX_ATTACHMENTS} attachments allowed (got ${items.length})`,
    );
  }
  for (const item of items) {
    if (item.size > MAX_FILE_BYTES) {
      throw new Error(
        `myconversation: attachment ${item.name} exceeds 20MB limit (${item.size} bytes)`,
      );
    }
  }
}
```

`src/media/classify.ts`:

```typescript
export type MediaKind = "image" | "document" | "video";

const IMAGE_EXT = new Set([
  ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".heif",
]);
const VIDEO_EXT = new Set([
  ".mp4", ".webm", ".mov", ".mkv", ".m4v",
]);

function extOf(path: string): string {
  const base = path.split(/[\\/]/).pop() ?? path;
  const dot = base.lastIndexOf(".");
  return dot >= 0 ? base.slice(dot).toLowerCase() : "";
}

export function classifyMediaKind(params: {
  path?: string;
  contentType?: string;
}): MediaKind {
  const ct = (params.contentType ?? "").trim().toLowerCase();
  if (ct.startsWith("image/")) return "image";
  if (ct.startsWith("video/")) return "video";
  if (ct) return "document";

  const ext = extOf(params.path ?? "");
  if (IMAGE_EXT.has(ext)) return "image";
  if (VIDEO_EXT.has(ext)) return "video";
  return "document";
}

export function bucketOutboundPaths(
  items: Array<{ path: string; contentType?: string }>,
): { images: string[]; files: string[]; skippedVideos: string[] } {
  const images: string[] = [];
  const files: string[] = [];
  const skippedVideos: string[] = [];
  for (const item of items) {
    const kind = classifyMediaKind(item);
    if (kind === "image") images.push(item.path);
    else if (kind === "video") skippedVideos.push(item.path);
    else files.push(item.path);
  }
  return { images, files, skippedVideos };
}
```

- [ ] **Step 4: Run tests**

```bash
pnpm test src/media/limits.test.ts src/media/classify.test.ts
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/media/limits.ts src/media/limits.test.ts src/media/classify.ts src/media/classify.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): add media classify and attachment limits

EOF
)"
```

---

### Task 3: Path helpers (TDD)

**Files:**
- Create: `src/media/paths.ts`
- Create: `src/media/paths.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
import { describe, expect, it } from "vitest";
import {
  isProtectedUploadPath,
  normalizeUploadPath,
  isExistingUploadPath,
  resolveMediaFetchUrl,
} from "./paths.js";

describe("normalizeUploadPath", () => {
  it("strips host from absolute upload URLs", () => {
    expect(
      normalizeUploadPath("https://gw.example.com/api/v1/upload/1/a.png"),
    ).toBe("api/v1/upload/1/a.png");
  });

  it("strips leading slash", () => {
    expect(normalizeUploadPath("/api/v1/upload/1/a.png")).toBe(
      "api/v1/upload/1/a.png",
    );
  });
});

describe("isProtectedUploadPath / isExistingUploadPath", () => {
  it("detects upload paths", () => {
    expect(isProtectedUploadPath("api/v1/upload/1/a.png")).toBe(true);
    expect(isExistingUploadPath("api/v1/upload/1/a.png")).toBe(true);
    expect(isExistingUploadPath("https://cdn.example.com/x.png")).toBe(false);
  });
});

describe("resolveMediaFetchUrl", () => {
  it("builds gateway URL for protected paths", () => {
    expect(
      resolveMediaFetchUrl("api/v1/upload/1/a.png", {
        endpoint: "https://gw.example.com",
      }),
    ).toEqual({
      url: "https://gw.example.com/api/v1/upload/1/a.png",
      auth: true,
    });
  });

  it("prefers staticUrl for protected paths when configured", () => {
    expect(
      resolveMediaFetchUrl("api/v1/upload/1/a.png", {
        endpoint: "https://gw.example.com",
        staticUrl: "https://s.example.com",
      }),
    ).toEqual({
      url: "https://s.example.com/api/v1/upload/1/a.png",
      auth: false,
      fallbackAuthUrl: "https://gw.example.com/api/v1/upload/1/a.png",
    });
  });

  it("passes through external absolute URLs without auth", () => {
    expect(
      resolveMediaFetchUrl("https://cdn.example.com/x.png", {
        endpoint: "https://gw.example.com",
      }),
    ).toEqual({ url: "https://cdn.example.com/x.png", auth: false });
  });
});
```

- [ ] **Step 2: Run to verify fail**

```bash
pnpm test src/media/paths.test.ts
```

- [ ] **Step 3: Implement `src/media/paths.ts`**

```typescript
import { normalizeGrpcBaseUrl } from "../connect/transport.js";

export function normalizeUploadPath(pathOrUrl: string): string {
  const trimmed = pathOrUrl.trim();
  if (!trimmed) return "";
  if (/^https?:\/\//i.test(trimmed)) {
    try {
      const url = new URL(trimmed);
      return `${url.pathname.replace(/^\//, "")}${url.search}`;
    } catch {
      return trimmed;
    }
  }
  return trimmed.replace(/^\//, "");
}

export function isProtectedUploadPath(pathOrUrl: string): boolean {
  const path = normalizeUploadPath(pathOrUrl);
  return path.startsWith("api/v1/upload/") || path.startsWith("upload/");
}

export function isExistingUploadPath(pathOrUrl: string): boolean {
  return isProtectedUploadPath(pathOrUrl);
}

export type MediaFetchTarget = {
  url: string;
  auth: boolean;
  fallbackAuthUrl?: string;
};

export function resolveMediaFetchUrl(
  pathOrUrl: string,
  opts: { endpoint: string; staticUrl?: string },
): MediaFetchTarget {
  const trimmed = pathOrUrl.trim();
  if (!trimmed) {
    throw new Error("myconversation: empty media path");
  }

  if (/^https?:\/\//i.test(trimmed) && !isProtectedUploadPath(trimmed)) {
    return { url: trimmed, auth: false };
  }

  const path = normalizeUploadPath(trimmed);
  const base = normalizeGrpcBaseUrl(opts.endpoint).replace(/\/+$/, "");
  const gatewayUrl = `${base}/${path}`;

  const staticBase = opts.staticUrl?.replace(/\/+$/, "");
  if (staticBase && isProtectedUploadPath(path)) {
    return {
      url: `${staticBase}/${path}`,
      auth: false,
      fallbackAuthUrl: gatewayUrl,
    };
  }

  return { url: gatewayUrl, auth: true };
}
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
pnpm test src/media/paths.test.ts
```

- [ ] **Step 5: Commit**

```bash
git add src/media/paths.ts src/media/paths.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): add media path normalize and fetch URL helpers

EOF
)"
```

---

### Task 4: myEdge client + multipart upload (TDD)

**Files:**
- Create: `src/connect/myedge.ts`
- Create: `src/media/upload.ts`
- Create: `src/media/upload.test.ts`

- [ ] **Step 1: Write failing upload tests (mock client)**

```typescript
import { describe, expect, it, vi } from "vitest";
import { uploadBuffer } from "./upload.js";

describe("uploadBuffer", () => {
  it("creates multipart, puts parts, completes, returns object key", async () => {
    const put = vi.fn().mockResolvedValue('"etag-1"');
    const edge = {
      createMultipartUpload: vi.fn().mockResolvedValue({
        uploadId: "up-1",
        objectKey: "api/v1/upload/92/1_uuid.png",
        parts: [{ partNumber: 1, url: "https://r2/part1" }],
      }),
      completeMultipartUpload: vi.fn().mockResolvedValue({}),
      abortMultipartUpload: vi.fn().mockResolvedValue({}),
      putPart: put,
    };

    const key = await uploadBuffer({
      edge: edge as never,
      userId: "92",
      fileName: "photo.png",
      contentType: "image/png",
      body: Buffer.from("hello"),
      putPart: async (url, body) => put(url, body),
    });

    expect(key).toBe("api/v1/upload/92/1_uuid.png");
    expect(edge.createMultipartUpload).toHaveBeenCalledOnce();
    expect(edge.completeMultipartUpload).toHaveBeenCalledOnce();
    expect(put).toHaveBeenCalledOnce();
  });

  it("aborts multipart on failure", async () => {
    const edge = {
      createMultipartUpload: vi.fn().mockResolvedValue({
        uploadId: "up-1",
        objectKey: "api/v1/upload/92/x.png",
        parts: [{ partNumber: 1, url: "https://r2/part1" }],
      }),
      completeMultipartUpload: vi.fn(),
      abortMultipartUpload: vi.fn().mockResolvedValue({}),
    };

    await expect(
      uploadBuffer({
        edge: edge as never,
        userId: "92",
        fileName: "photo.png",
        contentType: "image/png",
        body: Buffer.from("hello"),
        putPart: async () => {
          throw new Error("put failed");
        },
      }),
    ).rejects.toThrow("put failed");

    expect(edge.abortMultipartUpload).toHaveBeenCalledWith({
      objectKey: "api/v1/upload/92/x.png",
      uploadId: "up-1",
    });
  });
});
```

- [ ] **Step 2: Run to verify fail**

```bash
pnpm test src/media/upload.test.ts
```

- [ ] **Step 3: Implement myEdge client + upload**

`src/connect/myedge.ts` — mirror `createMyConversationTransport` auth, but create a `MyEdge` promise client:

```typescript
import { createPromiseClient, type PromiseClient } from "@connectrpc/connect";
import { MyEdge } from "@genjutsu/myedge-connect/myedge_connect";
import type { MyConversationChannelConfig } from "../config.js";
import { createMyConversationTransport } from "./transport.js";

export type MyEdgeClient = PromiseClient<typeof MyEdge>;

export function createMyEdgeClient(
  config: MyConversationChannelConfig,
): MyEdgeClient {
  // Reuse the same baseUrl + auth interceptor as myconversation RPCs.
  const transport = createMyConversationTransport(config);
  return createPromiseClient(MyEdge, transport);
}
```

If the package export path differs (`myedge_connect` vs another), adjust to match installed `@genjutsu/myedge-connect` (inspect `node_modules/@genjutsu/myedge-connect/package.json` exports).

`src/media/upload.ts`:

```typescript
import { randomUUID } from "node:crypto";

export const MULTIPART_PART_SIZE = 10 * 1024 * 1024;
export const MULTIPART_PART_CONCURRENCY = 4;

export type MyEdgeUploadApi = {
  createMultipartUpload(req: {
    fileName: string;
    contentType: string;
    objectKey: string;
    partCount: number;
  }): Promise<{
    uploadId: string;
    objectKey?: string;
    parts: Array<{ partNumber: number; url: string }>;
  }>;
  completeMultipartUpload(req: {
    objectKey: string;
    uploadId: string;
    parts: Array<{ partNumber: number; etag: string }>;
  }): Promise<unknown>;
  abortMultipartUpload(req: {
    objectKey: string;
    uploadId: string;
  }): Promise<unknown>;
  presignUploadParts?(req: {
    objectKey: string;
    uploadId: string;
    partNumbers: number[];
  }): Promise<{ parts: Array<{ partNumber: number; url: string }> }>;
};

export function buildObjectKey(userId: string, fileName: string): string {
  const ext = fileName.includes(".")
    ? fileName.slice(fileName.lastIndexOf(".") + 1)
    : "bin";
  return `api/v1/upload/${userId}/${Date.now()}_${randomUUID()}.${ext}`;
}

export async function uploadBuffer(params: {
  edge: MyEdgeUploadApi;
  userId: string;
  fileName: string;
  contentType: string;
  body: Buffer;
  putPart: (url: string, body: Buffer) => Promise<string>;
  signal?: AbortSignal;
}): Promise<string> {
  const objectKey = buildObjectKey(params.userId, params.fileName);
  const partCount = Math.max(
    1,
    Math.ceil(params.body.length / MULTIPART_PART_SIZE),
  );

  let uploadId = "";
  let key = objectKey;

  try {
    const created = await params.edge.createMultipartUpload({
      fileName: params.fileName,
      contentType: params.contentType || "application/octet-stream",
      objectKey,
      partCount,
    });
    uploadId = created.uploadId;
    key = created.objectKey || objectKey;

    const urlByPart = new Map(
      created.parts.map((p) => [p.partNumber, p.url] as const),
    );
    const etags: string[] = new Array(partCount);
    let nextPart = 0;

    const worker = async () => {
      while (nextPart < partCount) {
        if (params.signal?.aborted) {
          throw new Error("myconversation: upload aborted");
        }
        const idx = nextPart;
        nextPart += 1;
        const partNumber = idx + 1;
        const start = idx * MULTIPART_PART_SIZE;
        const chunk = params.body.subarray(
          start,
          start + MULTIPART_PART_SIZE,
        );
        etags[idx] = await params.putPart(
          urlByPart.get(partNumber) ?? "",
          Buffer.from(chunk),
        );
      }
    };

    const workers = Math.min(MULTIPART_PART_CONCURRENCY, partCount);
    await Promise.all(Array.from({ length: workers }, () => worker()));

    await params.edge.completeMultipartUpload({
      objectKey: key,
      uploadId,
      parts: etags.map((etag, i) => ({ partNumber: i + 1, etag })),
    });
    return key;
  } catch (error) {
    if (uploadId) {
      void params.edge
        .abortMultipartUpload({ objectKey: key, uploadId })
        .catch(() => undefined);
    }
    throw error;
  }
}

/** Default HTTP PUT for R2 presigned part URLs; returns ETag. */
export async function putPartHttp(
  url: string,
  body: Buffer,
  signal?: AbortSignal,
): Promise<string> {
  const res = await fetch(url, { method: "PUT", body, signal });
  if (!res.ok) {
    throw new Error(`myconversation: R2 part PUT failed: ${res.status}`);
  }
  const etag = res.headers.get("ETag");
  if (!etag) {
    throw new Error("myconversation: missing ETag on part response");
  }
  return etag;
}
```

Add a thin wrapper used by production code:

```typescript
export async function uploadFileForAccount(params: {
  edge: MyEdgeUploadApi;
  userId: string;
  fileName: string;
  contentType: string;
  body: Buffer;
  signal?: AbortSignal;
}): Promise<string> {
  return uploadBuffer({
    ...params,
    putPart: (url, body) => putPartHttp(url, body, params.signal),
  });
}
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
pnpm test src/media/upload.test.ts
```

- [ ] **Step 5: Commit**

```bash
git add src/connect/myedge.ts src/media/upload.ts src/media/upload.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): add myEdge multipart upload helper

EOF
)"
```

---

### Task 5: Inbound download + context (TDD)

**Files:**
- Create: `src/media/download.ts`
- Create: `src/media/context.ts`
- Create: `src/media/download.test.ts`
- Create: `src/media/context.test.ts`

- [ ] **Step 1: Write failing tests**

`src/media/context.test.ts`:

```typescript
import { describe, expect, it } from "vitest";
import { appendMediaContextLines, buildInboundMediaBody } from "./context.js";

describe("buildInboundMediaBody", () => {
  it("appends success and failure lines after content", () => {
    const body = buildInboundMediaBody({
      content: "hello",
      results: [
        {
          kind: "image",
          originalPath: "api/v1/upload/1/a.png",
          localPath: "/tmp/a.png",
          ok: true,
        },
        {
          kind: "document",
          originalPath: "api/v1/upload/1/b.pdf",
          ok: false,
        },
      ],
    });
    expect(body).toContain("hello");
    expect(body).toContain("[Ảnh: /tmp/a.png]");
    expect(body).toContain("[Tệp không tải được: api/v1/upload/1/b.pdf]");
  });
});
```

`src/media/download.test.ts` — mock `fetch` / inject `fetcher`:

```typescript
import { describe, expect, it, vi, afterEach } from "vitest";
import { mkdtemp, rm, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { downloadInboundAttachments, cleanupTempDir } from "./download.js";

afterEach(async () => {
  // tests create dirs under os.tmpdir — cleaned in each test finally
});

describe("downloadInboundAttachments", () => {
  it("writes successful downloads and skips oversize", async () => {
    const root = await mkdtemp(join(tmpdir(), "myconv-dl-"));
    try {
      const fetcher = vi.fn(async (url: string) => {
        if (url.includes("big")) {
          return {
            ok: true,
            headers: { get: (h: string) => (h === "content-length" ? String(21 * 1024 * 1024) : null) },
            arrayBuffer: async () => new ArrayBuffer(0),
          };
        }
        return {
          ok: true,
          headers: { get: () => null },
          arrayBuffer: async () => Uint8Array.from([1, 2, 3]).buffer,
        };
      });

      const results = await downloadInboundAttachments({
        attachments: [
          { kind: "image", path: "api/v1/upload/1/ok.png" },
          { kind: "document", path: "api/v1/upload/1/big.pdf" },
        ],
        account: {
          endpoint: "https://gw.example.com",
          tenantId: "t",
          token: "tok",
        },
        tempRoot: root,
        messageId: "99",
        fetcher: fetcher as never,
      });

      expect(results[0]?.ok).toBe(true);
      expect(results[0]?.localPath).toBeTruthy();
      const bytes = await readFile(results[0]!.localPath!);
      expect(bytes.equals(Buffer.from([1, 2, 3]))).toBe(true);
      expect(results[1]?.ok).toBe(false);
    } finally {
      await cleanupTempDir(root);
    }
  });
});
```

- [ ] **Step 2: Run to verify fail**

```bash
pnpm test src/media/context.test.ts src/media/download.test.ts
```

- [ ] **Step 3: Implement**

`src/media/context.ts`:

```typescript
import type { InboundAttachmentRef } from "./limits.js";

export type InboundDownloadResult = InboundAttachmentRef & {
  ok: boolean;
  localPath?: string;
  originalPath: string;
  error?: string;
};

export function appendMediaContextLines(
  results: InboundDownloadResult[],
): string[] {
  const lines: string[] = [];
  for (const r of results) {
    if (r.ok && r.localPath) {
      lines.push(
        r.kind === "image"
          ? `[Ảnh: ${r.localPath}]`
          : `[Tệp: ${r.localPath}]`,
      );
    } else {
      lines.push(
        r.kind === "image"
          ? `[Ảnh không tải được: ${r.originalPath}]`
          : `[Tệp không tải được: ${r.originalPath}]`,
      );
    }
  }
  return lines;
}

export function buildInboundMediaBody(params: {
  content: string;
  results: InboundDownloadResult[];
}): string {
  const lines = appendMediaContextLines(params.results);
  if (lines.length === 0) return params.content;
  if (!params.content.trim()) return lines.join("\n");
  return `${params.content}\n${lines.join("\n")}`;
}

export function successfulLocalPaths(
  results: InboundDownloadResult[],
): string[] {
  return results
    .filter((r) => r.ok && r.localPath)
    .map((r) => r.localPath!);
}
```

`src/media/download.ts` — implement:

- `defaultMediaTempRoot(account)` → `account.mediaTempDir ?? join(tmpdir(), "openclaw-myconversation")`
- `downloadInboundAttachments`: create `{tempRoot}/{messageId}-{uuid}/`, for each attachment resolve URL via `resolveMediaFetchUrl`, fetch with optional `Authorization` + `x-tenant-id`, enforce `MAX_FILE_BYTES` via Content-Length or buffer length, write file with safe basename
- On staticUrl miss (non-ok), retry `fallbackAuthUrl` with auth
- `cleanupTempDir(dir)` → `rm(dir, { recursive: true, force: true })`

Require `userId` only for outbound upload; inbound download uses tenant token (auth headers), not object-key userId.

- [ ] **Step 4: Run tests — PASS**

```bash
pnpm test src/media/context.test.ts src/media/download.test.ts
```

- [ ] **Step 5: Commit**

```bash
git add src/media/download.ts src/media/context.ts src/media/download.test.ts src/media/context.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): add inbound media download and agent context lines

EOF
)"
```

---

### Task 6: File-only + first-chunk media in `sendChatGroupReplyChunked` (TDD)

**Files:**
- Modify: `src/outbound/reply.ts`
- Modify: `src/outbound/reply.test.ts`

- [ ] **Step 1: Write failing tests**

Add to `src/outbound/reply.test.ts`:

```typescript
it("sends file-only message when text is empty but files present", async () => {
  const sendChatGroupMessage = vi
    .fn()
    .mockResolvedValue(makeMessage(99, ""));
  const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

  await sendChatGroupReplyChunked(client, {
    groupId: 16,
    text: "   ",
    files: ["api/v1/upload/92/a.pdf"],
  });

  expect(sendChatGroupMessage).toHaveBeenCalledOnce();
  expect(sendChatGroupMessage.mock.calls[0][0].content).toBe("");
  expect(sendChatGroupMessage.mock.calls[0][0].files).toEqual([
    "api/v1/upload/92/a.pdf",
  ]);
});

it("attaches images/files only on the first chunk", async () => {
  const longText = "x".repeat(5000);
  const sendChatGroupMessage = vi
    .fn()
    .mockResolvedValueOnce(makeMessage(1, "a"))
    .mockResolvedValueOnce(makeMessage(2, "b"));
  const client = { sendChatGroupMessage } as unknown as MyConversationConnectClient;

  await sendChatGroupReplyChunked(client, {
    groupId: 16,
    text: longText,
    images: ["api/v1/upload/92/a.png"],
    files: ["api/v1/upload/92/a.pdf"],
  });

  expect(sendChatGroupMessage.mock.calls[0][0].images).toEqual([
    "api/v1/upload/92/a.png",
  ]);
  expect(sendChatGroupMessage.mock.calls[0][0].files).toEqual([
    "api/v1/upload/92/a.pdf",
  ]);
  expect(sendChatGroupMessage.mock.calls[1][0].images).toEqual([]);
  expect(sendChatGroupMessage.mock.calls[1][0].files).toEqual([]);
});
```

- [ ] **Step 2: Run to verify fail**

```bash
pnpm test src/outbound/reply.test.ts
```

Expected: FAIL on file-only (current early return skips RPC).

- [ ] **Step 3: Fix `sendChatGroupReplyChunked`**

Replace empty-text early return with:

```typescript
export async function sendChatGroupReplyChunked(
  client: MyConversationConnectClient,
  params: ChatGroupReplyParams,
): Promise<SendChatGroupMessageReplyType> {
  const chunks = chunkChatGroupReplyText(params.text);
  const hasMedia =
    (params.images?.length ?? 0) > 0 ||
    (params.videos?.length ?? 0) > 0 ||
    (params.files?.length ?? 0) > 0;

  if (chunks.length === 0 && !hasMedia) {
    return new SendChatGroupMessageReply({ duplicate: false });
  }

  if (chunks.length === 0 && hasMedia) {
    return sendChatGroupReply(client, {
      groupId: params.groupId,
      text: "",
      images: params.images,
      videos: params.videos,
      files: params.files,
      mentionedUserIds: params.mentionedUserIds,
    });
  }

  let lastReply: SendChatGroupMessageReplyType | undefined;
  for (let i = 0; i < chunks.length; i++) {
    lastReply = await sendChatGroupReply(client, {
      groupId: params.groupId,
      text: chunks[i],
      images: i === 0 ? params.images : undefined,
      videos: i === 0 ? params.videos : undefined,
      files: i === 0 ? params.files : undefined,
      mentionedUserIds: i === 0 ? params.mentionedUserIds : undefined,
    });
  }
  return lastReply!;
}
```

Note: when `images`/`files` are `undefined` on later chunks, `sendChatGroupReply` already defaults to `[]` — tests should expect `[]` (or update `sendChatGroupReply` to pass through empty arrays explicitly; current code uses `params.images ?? []`).

- [ ] **Step 4: Run tests — PASS**

```bash
pnpm test src/outbound/reply.test.ts
```

- [ ] **Step 5: Commit**

```bash
git add src/outbound/reply.ts src/outbound/reply.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): allow file-only chat group replies

EOF
)"
```

---

### Task 7: Outbound media orchestration (TDD)

**Files:**
- Create: `src/media/outbound.ts`
- Create: `src/media/outbound.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
import { describe, expect, it, vi } from "vitest";
import { prepareOutboundMedia } from "./outbound.js";

describe("prepareOutboundMedia", () => {
  it("passes through existing upload paths without upload", async () => {
    const upload = vi.fn();
    const result = await prepareOutboundMedia({
      userId: "92",
      mediaUrls: ["api/v1/upload/92/a.png", "api/v1/upload/92/b.pdf"],
      uploadFile: upload,
      readLocalFile: async () => Buffer.from(""),
    });
    expect(upload).not.toHaveBeenCalled();
    expect(result.images).toEqual(["api/v1/upload/92/a.png"]);
    expect(result.files).toEqual(["api/v1/upload/92/b.pdf"]);
    expect(result.skippedVideos).toEqual([]);
  });

  it("uploads local files and buckets by MIME", async () => {
    const upload = vi
      .fn()
      .mockResolvedValueOnce("api/v1/upload/92/new.png")
      .mockResolvedValueOnce("api/v1/upload/92/new.pdf");
    const result = await prepareOutboundMedia({
      userId: "92",
      mediaUrls: ["/tmp/a.png", "/tmp/b.pdf"],
      uploadFile: upload,
      readLocalFile: async (p) =>
        Buffer.from(p.endsWith(".png") ? "img" : "pdf"),
      contentTypeForPath: (p) =>
        p.endsWith(".png") ? "image/png" : "application/pdf",
    });
    expect(upload).toHaveBeenCalledTimes(2);
    expect(result.images).toEqual(["api/v1/upload/92/new.png"]);
    expect(result.files).toEqual(["api/v1/upload/92/new.pdf"]);
  });

  it("skips videos and rejects >5 attachments", async () => {
    await expect(
      prepareOutboundMedia({
        userId: "92",
        mediaUrls: ["a", "b", "c", "d", "e", "f"],
        uploadFile: async () => "x",
        readLocalFile: async () => Buffer.from("x"),
      }),
    ).rejects.toThrow(/5/);
  });
});
```

- [ ] **Step 2: Run to verify fail**

```bash
pnpm test src/media/outbound.test.ts
```

- [ ] **Step 3: Implement `src/media/outbound.ts`**

Logic:

1. Normalize `mediaUrls` (also accept single `mediaUrl`)
2. `assertOutboundAttachmentLimits` after resolving sizes for local/http sources; existing upload paths count as size 0 for limit-by-count only (still count toward 5)
3. For each URL:
   - if `isExistingUploadPath` → use `normalizeUploadPath`, classify by extension
   - else if `http(s)` → download with size cap → upload
   - else treat as local path → `readLocalFile` → upload
4. Skip `video` kinds into `skippedVideos` (do not upload)
5. Return `{ images, files, skippedVideos }`

Require non-empty `userId` before any upload; throw clear error if missing.

- [ ] **Step 4: Run tests — PASS**

```bash
pnpm test src/media/outbound.test.ts
```

- [ ] **Step 5: Commit**

```bash
git add src/media/outbound.ts src/media/outbound.test.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): add outbound media prepare/upload orchestration

EOF
)"
```

---

### Task 8: Wire inbound `dispatch.ts`

**Files:**
- Modify: `src/inbound/dispatch.ts`

- [ ] **Step 1: After mention gate passes, before `finalizeInboundContext`**

1. If `message.videos?.length`, `log.debug` with `skipped-videos` and count.
2. `selectInboundAttachments({ images: message.images, files: message.files })`.
3. If selected length > 0, call `downloadInboundAttachments(...)` into a temp dir; keep `tempDir` for cleanup.
4. Build `agentBody = buildInboundMediaBody({ content: rawBody, results })`.
5. `mediaPaths = successfulLocalPaths(results)`.

- [ ] **Step 2: Pass into context**

```typescript
const ctxPayload = reply.finalizeInboundContext({
  Body: body, // envelope may still use rawBody or agentBody — prefer agentBody in BodyForAgent
  BodyForAgent: agentBody,
  RawBody: agentBody,
  CommandBody: rawBody, // keep commands based on original text without media lines
  // ...existing fields...
  MediaPaths: mediaPaths.length > 0 ? mediaPaths : undefined,
}) as FinalizedMsgContext;
```

Use OpenClaw field name `MediaPaths` (confirmed in SDK `channel-inbound` / reply types).

- [ ] **Step 3: Update `deliver` callback**

```typescript
deliver: async (payload) => {
  const text = String(payload.text ?? "");
  const mediaUrls =
    (payload as { mediaUrls?: string[] }).mediaUrls ??
    ((payload as { mediaUrl?: string }).mediaUrl
      ? [(payload as { mediaUrl: string }).mediaUrl]
      : []);
  if (!text.trim() && mediaUrls.length === 0) {
    return;
  }

  if (!account.userId && mediaUrls.length > 0) {
    throw new Error(
      "myconversation: userId is required to upload outbound media",
    );
  }

  let images: string[] = [];
  let files: string[] = [];
  if (mediaUrls.length > 0) {
    const edge = createMyEdgeClient(account);
    const prepared = await prepareOutboundMedia({
      userId: account.userId!,
      mediaUrls,
      uploadFile: (args) =>
        uploadFileForAccount({ edge, userId: account.userId!, ...args }),
      readLocalFile: async (p) => readFile(p),
    });
    for (const v of prepared.skippedVideos) {
      log.warn?.("myconversation: skipped outbound video", { path: v });
    }
    images = prepared.images;
    files = prepared.files;
  }

  const sent = await sendChatGroupReplyChunked(unaryClient, {
    groupId,
    text,
    images,
    files,
  });
  // ...existing logging...
},
```

- [ ] **Step 4: Cleanup temp dir in `finally`**

Wrap the existing try/finally so after `typingSession.stop()` also `await cleanupTempDir(tempDir)` when set.

- [ ] **Step 5: Typecheck + unit tests**

```bash
pnpm test
pnpm run typecheck
```

Expected: PASS (may need small type casts on payload).

- [ ] **Step 6: Commit**

```bash
git add src/inbound/dispatch.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): wire inbound download and outbound media deliver

EOF
)"
```

---

### Task 9: Wire `channel.ts` `sendMedia` + enable capability

**Files:**
- Modify: `src/channel.ts`

- [ ] **Step 1: Set capability**

```typescript
capabilities: {
  chatTypes: ["group"],
  media: true,
},
```

- [ ] **Step 2: Add `attachedResults.sendMedia`**

OpenClaw `ChannelOutboundContext` provides `to`, `text`, `mediaUrl`, optional `mediaReadFile`. Implement:

```typescript
sendMedia: async ({
  cfg,
  to,
  text,
  mediaUrl,
  accountId,
  mediaReadFile,
}) => {
  const account = resolveMyConversationAccount(cfg, accountId);
  if (!account.userId) {
    throw new Error(
      "myconversation: userId is required to upload outbound media",
    );
  }
  const client = resolveClientForAccount(account);
  const groupId = resolveGroupIdFromOutboundParams({ to, text });
  const edge = createMyEdgeClient(account);
  const prepared = await prepareOutboundMedia({
    userId: account.userId,
    mediaUrls: mediaUrl ? [mediaUrl] : [],
    uploadFile: (args) =>
      uploadFileForAccount({ edge, userId: account.userId!, ...args }),
    readLocalFile: async (p) =>
      mediaReadFile ? mediaReadFile(p) : readFile(p),
  });
  const reply = await sendChatGroupReplyChunked(client, {
    groupId,
    text: String(text ?? ""),
    images: prepared.images,
    files: prepared.files,
  });
  return {
    messageId: String(reply.message?.id ?? ""),
    // channel field may be injected by SDK wrapper — match sendText return shape
  };
},
```

Keep `sendText` as-is (text-only). If OpenClaw also sends media via `sendText`+payload in some paths, Task 8 `deliver` already covers inbound-reply path.

- [ ] **Step 3: Typecheck**

```bash
pnpm run typecheck
pnpm test
```

- [ ] **Step 4: Commit**

```bash
git add src/channel.ts
git commit -m "$(cat <<'EOF'
feat(myconversation): enable media capability and sendMedia outbound

EOF
)"
```

---

### Task 10: README + gateway start warning

**Files:**
- Modify: `README.md`
- Modify: `src/gateway.ts` (or account start path) — warn if media-capable but `userId` missing

- [ ] **Step 1: README section**

Add after Config notes:

```markdown
## Media (images + files)

- Bidirectional: staff attachments are downloaded to a local temp dir and passed to the agent as `MediaPaths`; agent media replies are uploaded via **myEdge multipart** then sent as `images[]` / `files[]` on `SendChatGroupMessage`.
- **Supported:** images and documents. **Not supported (v1):** videos (inbound skipped; outbound skipped with warning).
- **Limits:** max 5 attachments per message; 20MB per file.
- **`userId` is required** for outbound uploads (object key prefix).
- Optional `staticUrl`: public static host for inbound reads (fallback to authenticated gateway fetch).
- Optional `mediaTempDir`: override temp root (default `{os.tmpdir()}/openclaw-myconversation`).
```

Update Status bullet that said media can be expanded later.

- [ ] **Step 2: Warn at gateway start**

In `startMyConversationGatewayAccount` (or equivalent), if `!account.userId`, `log.warn("myconversation: userId missing; outbound media uploads will fail")`.

- [ ] **Step 3: Commit**

```bash
git add README.md src/gateway.ts
git commit -m "$(cat <<'EOF'
docs(myconversation): document media send/receive behavior

EOF
)"
```

---

### Task 11: Full verification

- [ ] **Step 1: Run full suite**

```bash
cd /Users/nemo/go/src/gitlab.genjutsu.ai/marketplace/openclaw/myconversation
pnpm test
pnpm run typecheck
pnpm run build
```

Expected: all PASS; `dist/` builds.

- [ ] **Step 2: Manual E2E checklist** (record results in PR / chat)

1. Staff: image + `@bot` → agent sees local path in context
2. Agent: reply with file → helpdesk shows attachment
3. File-only inbound with mention → agent runs
4. Inbound video → ignored; text still works
5. File > 20MB → skipped without crash

- [ ] **Step 3: Final commit only if leftover docs/fixes**

---

## Spec coverage self-check

| Spec requirement | Task |
|------------------|------|
| Bidirectional images + files | 8, 9 |
| No outbound video; inbound video skip | 2, 7, 8 |
| myEdge multipart upload | 4, 7 |
| Inbound download to temp + MediaPaths | 5, 8 |
| Limits 5 / 20MB | 2, 5, 7 |
| File-only send | 6 |
| Attachments first chunk only | 6 |
| Config `staticUrl` / `mediaTempDir` | 1 |
| `userId` required for upload | 7, 8, 9, 10 |
| No Go backend changes | (none) |
| README | 10 |
| Unit tests | 2–7 |
| Manual E2E | 11 |

## Placeholder / consistency check

- OpenClaw fields locked: inbound `MediaPaths`; outbound `mediaUrl` / `mediaUrls`; hook `attachedResults.sendMedia`.
- myEdge package pin: `^1.1.0` (helpdesk).
- Object key format matches helpdesk: `api/v1/upload/{userId}/{ts}_{uuid}.{ext}`.
